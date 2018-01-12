import sys
import subprocess
from subprocess import PIPE
from lxml import etree
import os.path
import argparse
import functools

# new version for osc-core in the master branch
core_master_version = "1.2.0-SNAPSHOT"
# new version for the sdn ctrlr SDK and plugins in the master branch
sdn_ctrlr_api_master_version = "3.0.1-SNAPSHOT"
# new version for the security mgr SDK and plugins in the master branch
sec_mgr_api_master_version = "3.0.1-SNAPSHOT"
# new version for osc-core in the release branch
core_release_version = "0.9.0"
# new version for the sdn ctrlr SDK and plugins in the release branch
sdn_ctrlr_api_release_version = "3.0.0"
# new version for the security mgr SDK and plugins in the release branch
sec_mgr_api_release_version = "3.0.0"

print = functools.partial(print, flush=True)

core_projects = [
            "osc-common",
            "osc-control",
            "osc-domain",
            "osc-export",
            "osc-installer",
            "osc-installer-simple",
            "osc-installer-test",
            "osc-resolver",
            "osc-rest-server",
            "osc-server",
            "osc-service-api",
            "osc-tools",
            "osc-uber",
            "osc-uber-kubernetes",
            "osc-uber-openstack4j",
            "osc-ui",
            "osc-ui-widgetset",
            ]

# Represents a repo and its versions
class Repo:
    def __init__(self, name, version, sec_mgr_version, sdn_ctrlr_version):
        self.name = name  # name of the repo
        self.version = version # version of the repo to be used in the pom.xml, branch name, git tag, ...
        self.sec_mgr_version = sec_mgr_version # version of the security mgr SDK to be used in the dependencies
        self.sdn_ctlr_version = sdn_ctrlr_version # version of the SDN ctrlr  SDK to be used in the dependencies

    # Creates a new release branch with the updated and committed pom
    # according to the version information in self
    def prepare_release_branch(self):
        print("Creating the release branch for {}\n".format(self))

        # Creating the release branch
        self.process_run(p_args=["git", "checkout", "-b", self.version])

        # Creating the version commit with modified pom
        self.create_version_commit()

        # Upstreaming the release branch
        self.process_run(p_args=["git", "push", "upstream", self.version])

        print('\n')

    # Creates a snapshot release in the master branch of the
    # targeted repo with the version information in self
    def create_snapshot(self):
        print("Creating the snapshot for {}\n".format(self))

        # Creating the version commit with the pom modified for the new versions
        self.create_version_commit()

        # Upstreaming the snapshot version commit
        self.process_run(p_args=["git", "push", "upstream", "master", "--no-verify"])

        # Tagging the commit with the target snapshot version
        self.create_tag()

        print('\n')

    # Creates the version commit representing the version
    # in self.
    def create_version_commit(self):
        # Updating the pom with the new versions
        self.update_pom()

        pom_file = "pom.xml"
        self.process_run(p_args=["git", "add", pom_file])

        # For the osc-core repo also update each project pom
        if self.name == "osc-core":
            for core_project in core_projects:
                self.update_pom(core_project)

                core_project_pom_file = core_project + "/" + pom_file

                self.process_run(["git", "add", core_project_pom_file])

        # Creating the version commit
        self.process_run(p_args=["git", "commit", "-m", "Version {}".format(self.version)])

    # Tags the HEAD of the current branch with the self.version
    # and upstreams
    def create_tag(self):
        self.process_run(["git", "tag", "-a", "v"+self.version, "-m", "Version {}".format(self.version)])
        self.process_run(["git", "push", "origin", "--tags", "-f"]) #upstream
        self.process_run(["git", "describe", "--long"])

    # Updates the pom.xml file (or project/pom.xml, if project_name is provided)
    # with the new versions
    def update_pom(self, project_name=None):
        eparser = etree.XMLParser(remove_comments=False)
        pom_file = "/pom.xml"
        if project_name is not None:
            pom_file = self.name + "/" + project_name + pom_file
        else:
            pom_file = self.name + pom_file

        print("Updating the pom {}".format(pom_file))
        pom_xml = etree.parse(pom_file, parser=eparser)

        # XML elements to be updated in the pom.xml file if found:
        # version, parent version, sdn ctrlr dependency, security mgr dependency
        version = pom_xml.find("{*}version")
        parent_version = pom_xml.find("{*}parent/{*}version")
        sdn_ctrlr_dep_version = pom_xml.find("{*}dependencies/{*}dependency[{*}artifactId='sdn-controller-api']/{*}version")
        sec_mgr_dep_version = pom_xml.find("{*}dependencies/{*}dependency[{*}artifactId='security-mgr-api']/{*}version")

        if version is not None:
            version.text = self.version
        else:
            print("'version' tag not found in the pom {}".format(pom_file))

        if parent_version is not None:
            parent_version.text = self.version
        else:
            print("'parent/version' tag not found in the pom {}".format(pom_file))

        if sdn_ctrlr_dep_version is not None:
            sdn_ctrlr_dep_version.text = self.sdn_ctlr_version
        else:
            print("sdn ctrlr dependency not found in the pom {}".format(pom_file))

        if sec_mgr_dep_version is not None:
            sec_mgr_dep_version.text = self.sec_mgr_version
        else:
            print("sec mgr dependency not found in the pom {}".format(pom_file))

        # Writing the updated xml in the pom file
        with open(pom_file, 'wb') as f:
            f.write(etree.tostring(pom_xml.getroot()))

        # Add the header in the pom file. Although all the other XML comments are preserved
        # it seems the header is being removed. This preserves the header.
        if self.name not in ("osc-pan-plugin", "osc-nuage-plugin"):
            add_header(pom_file)

    # Cleans up the local repository deleting the
    # created release branch, tag and hard resetting the master branch
    def cleanup(self):
        print("Cleaning up the {}\n".format(self))

        # Deleting the release branch
        self.process_run(p_args=["git", "fetch", "upstream"])
        self.process_run(p_args=["git", "checkout", "master"])
        self.process_run(p_args=["git", "reset", "--hard", "upstream/master"])
        self.process_run(p_args=["git", "branch", "-D", self.version])

        # Deleting the release tag
        p1 = self.process_Popen(p_args=["git", "tag", "-l"], p_stdout=PIPE)
        p2 = self.pipe_in_process_Popen(p_args=["xargs", "git", "tag", "-d"], p_stdin=p1.stdout, p_stdout=PIPE)
        p1.stdout.close()
        print(p2.communicate()[0])

        self.process_run(p_args=["git", "fetch", "upstream", "-t"])
        self.process_run(p_args=["git", "tag", "-d", "v"+self.version])

        print('\n')

    def process_run(self, p_args):
        subprocess.run(args=p_args, cwd=self.name)

    def pipe_in_process_Popen(self, p_args, p_stdin, p_stdout):
        return subprocess.Popen(p_args, cwd=self.name, stdin=p_stdin, stdout=p_stdout)

    def process_Popen(self, p_args, p_stdout):
        return subprocess.Popen(p_args, cwd=self.name, stdout=p_stdout)

    def __str__(self):
        return "Repo {} with version {}, sec-mgr- version {}, sdn-ctrlr-version {}\n".format(self.name, self.version, self.sec_mgr_version, self.sdn_ctlr_version)

# Desired snapshot versions for each repo
repo_snapshots = [
            Repo("osc-core", core_master_version, sec_mgr_api_master_version, sdn_ctrlr_api_master_version),
            Repo("security-mgr-api", sec_mgr_api_master_version, "n/a", "n/a"),
            Repo("sdn-controller-api", sdn_ctrlr_api_master_version, "n/a", "n/a"),
            Repo("security-mgr-sample-plugin", sec_mgr_api_master_version, sec_mgr_api_master_version, "n/a"),
            Repo("osc-pan-plugin", sec_mgr_api_master_version, sec_mgr_api_master_version, "n/a"),
            Repo("sdn-controller-nsc-plugin", sdn_ctrlr_api_master_version, "n/a", sdn_ctrlr_api_master_version),
            Repo("sdn-controller-nsfc-plugin", sdn_ctrlr_api_master_version, "n/a", sdn_ctrlr_api_master_version),
            Repo("osc-nuage-plugin", sdn_ctrlr_api_master_version, "n/a", sdn_ctrlr_api_master_version),
        ]

# Desired release versions for each repo
repo_releases = [
            Repo("osc-core", core_release_version, sec_mgr_api_release_version, sdn_ctrlr_api_release_version),
            Repo("security-mgr-api", sec_mgr_api_release_version, "n/a", "n/a"),
            Repo("sdn-controller-api", sdn_ctrlr_api_release_version, "n/a", "n/a"),
            Repo("security-mgr-sample-plugin", sec_mgr_api_release_version, sec_mgr_api_release_version, "n/a"),
            Repo("osc-pan-plugin", sec_mgr_api_release_version, sec_mgr_api_release_version, "n/a"),
            Repo("sdn-controller-nsc-plugin", sdn_ctrlr_api_release_version, "n/a", sdn_ctrlr_api_release_version),
            Repo("sdn-controller-nsfc-plugin", sdn_ctrlr_api_release_version, "n/a", sdn_ctrlr_api_release_version),
            Repo("osc-nuage-plugin", sdn_ctrlr_api_release_version, "n/a", sdn_ctrlr_api_release_version),
        ]

def add_header(filename):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0,0)
        f.write("""<!--
    Copyright (c) Intel Corporation
    Copyright (c) 2017

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
 -->\n""" + content)

# Resets the local master with the upstream/master and cleans up all local residual
# like release branches, tags, modified poms, etc.
# Should be the first command executed prior to starting a release.
def cleanup():
    for repo_snapshot in repo_snapshots:
        repo_snapshot.cleanup()

    for repo_release in repo_releases:
        repo_release.cleanup()

# Creates a release branch for each OSC repo and upstreams them.
def prepare_release_branches():
    for repo_release in repo_releases:
        repo_release.prepare_release_branch()

# Creates a release tag for the release branches. Should be
# executed after 'prepare_release_branches'
def create_release_tags():
    for repo_release in repo_releases:
        repo_release.create_tag()

# Creates a snapshot release in the master branch of each OSC repo.
def create_snapshots():
    for repo_snapshot in repo_snapshots:
        repo_snapshot.create_snapshot()

FUNCTION_MAP = {'cleanup': cleanup,
                'branch-release': prepare_release_branches,
                'tag-release': create_release_tags,
                'create-snapshot': create_snapshots}

parser = argparse.ArgumentParser(description='Helpers script to create a release branch and tags for OSC repos')
parser.add_argument('command', choices=FUNCTION_MAP.keys())

args = parser.parse_args()
func = FUNCTION_MAP[args.command]
func()
