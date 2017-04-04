# Unit Test Conventions and Guidelines

## Introduction

This document outlines the code conventions and guidelines that must be followed when authoring unit tests for new and existing OSC components and features. Each of the topics covered in this section is aligned with the following core principles:

1. Isolation and independency: Tests should not be interdependent. They should run in any order and do not propagate failure.
2. Single responsibility: Each test should validate a single unit or aspect of the code.
3. Optimized for reading and maintaining: Tests should be written in a way that is easy to read and maintain. Do not optimize for authoring. A test is usually written once and read many times.
4. Consistency: Test name and format should be consistent across OSC.
5. Environment independent execution: A deployment must not be needed to execute the tests.
6. Run fast: A single test should run in a matter of tens of milliseconds. A test that is taking longer to run might be doing too much or have a hidden environment dependency.

## Conventions

### Test Location

The hierarchy and location of the unit tests should mirror the product code for consistency and easy maintenance. **ALL** the unit test code of a given component should be under **component_name\src\test**.

**DO:**

`osc-server\src\test\java\org\osc\core\broker\service\AddDistributedApplianceServiceTest.java`

**DON'T:**
 
`osc-server\src\java\org\osc\core\broker\service\AddDistributedApplianceServiceTest.java`

#### Test Classes

Every unit test class must have a respective product class. The sub-path of the test class under \src\test\ must fully match the class under test.

For instance, class under test: `vmiDCServer\src\java\org\osc\core\broker\service\AddDistributedApplianceService.java`

**DO:**

`osc-server\src\test\java\org\osc\core\broker\service\AddDistributedApplianceServiceTest.java`

**DON'T:**

`osc-server\src\java\org\osc\core\broker\AddDistributedApplianceServiceTest.java`

`osc-server\src\java\org\osc\core\broker\service\distributedappliance\AddDistributedApplianceServiceTest.java`

#### Supporting Code

Any supporting code (helpers, entities, validators, etc) meant to be used across tests within different packages should be within a package suffixed with **_.test.util**, and prefixed with the longest common path across the test code that will use it.

For instance, given the TestGraphHelper.java meant to be used by tests in the packages

`osc-server\src\java\org\osc\core\broker\service\tasks\*`

**DO:**

`osc-server\src\test\java\org\osc\core\broker\service\tasks\test\util\TaskGraphHelper.java`

**DON'T:**

`osc-server\src\java\org\osc\core\test\util\TaskGraphHelper.java`

`osc-server\src\java\org\osc\core\broker\service\tasks\TaskGraphHelper.java`

Any supporting code that is NOT meant to be used across tests in different packages must stay within the package that uses it. It should be made a private class if the code is used only by a single class.

Keep the code less visible when in doubt as to whether it will be used by other classes or packages in the future.

### Naming

#### Test Class Name

The name of the test class should match the class under tests with the addition of the suffix **Test**.

For instance, class under test: `AddDistributedApplianceService.java`

**DO:**

`AddDistributedApplianceServiceTest.java`

**DON'T:**

`AddDistributedApplianceServiceTests.java`

`TestsAddDistributedApplianceService`

`TestAddDistributedApplianceService.java`

`AddDistributedApplianceService.java`

#### Test Method Name

Keep the following in mind when authoring a unit test: 
* what is being tested
* how it is being tested
* what is the expectation being validated

Keeping these things in mind for each test will result in clear, small, and more maintainable test methods.

The naming convention adopted for the test methods highlights these things, making the test name self-explanatory with no need for additional documentation. Having difficulty naming a test method after these things likely indicates a code smell that might be trying to cover too much on a single unit test.

The test method name should follow this pattern:
```java
testMethodUnderTest_HowIsItTested_WhatItExpects(){}
```

With the exception of (**testMethodUnderTest**), free form is provided to allow for clarity if needed. 

For instance, if you are testing the following method:
```java
void depositCheck(string checkNumber, int value) throws Exception{}
```
**DO:**
```java
testDepositCheck_WithNegativeValue_ThrowsInvalidValueException(){}

testDepositCheck_WithValidValue_ExpectsSuccessDeposit(){}
```
**DON'T:**
```java
testDepositCheckWithNegativeValueThrowsInvalidValueException(){} // no clear separation

testDepositCheckNegativeValue(){} // no clear expectation

testDepositCheck(){} // too vague

testdepositCheck_WithValidValue_ExpectsSuccessDeposit(){} // lower case method name

depositCheck_WithValidValue_ExpectsSuccessDeposit(){} // no test prefix

testDeposit_WithValidValue_ExpectsSuccessDeposit(){} // wrong test method name
```
### Documentation

#### Test Class and Method

Documentation is unnecessary and rendundant for test classes and test methods with the proper naming conventions. Placing the emphasis on the name versus documentation not only makes the test code itself clear, but also does so within other areas (such as those shown below) that usually don&#39;t display documentation at a glance:

* IDEs
* build reports
* test result files

#### Arrange-Act-Assert

For details on Arrange-Act-Assert, see the Test Format session below. Adding the comments **// Arrange. // Act. // Assert.** within the body of your test method creates clear, visual boundaries within the test method, helping you organize the code and facilitate code reviews since it becomes very evident what is the core part of the test, what is being setup and how it is being validated. This is particularly useful for test methods with many arrange and assert lines. For short test methods these comments may not be necessary.

**DO:**

```java
// Arrange.
Request request = new Request();
Response expectedResponse = new Response();

// Act.
actualResponse = request.invoke();

// Assert.
Assert.assertNotNull(actualResponse);
Assert.assertEquals(this.expectedResponse, actualResponse);
```

**DON'T:**

```java
Request request = new Request();
Response expectedResponse = new Response();

actualResponse = request.invoke();

Assert.assertNotNull(actualResponse);
Assert.assertEquals(this.expectedResponse, actualResponse);
```

#### Supporting Code

Any supporting code that is used across different test classes should be documented with the same attention used for product code.

### Asserting

To validate test results use the methods offered by org.junit.Assert. Observe that most of the assertion methods have an overloaded flavor that takes a String to be used as a message when the assertion fails. **ALWAYS** use this version of the method, the error message is displayed when the test fails and this helps greatly to quickly identify the source of the error. Asserts within the same test method should never have the same message.

**DO:**
```java
Assert.assertEquals("The response id was different than expected.", expectedId, response.getId());
```
**DON'T:**
```java
Assert.assertEquals(daId, response.getId()) // No message

Assert.assertEquals("Unexpected result.", daId, response.getId()); // Too generic
```
Additionally, observe the order of the parameters. The first parameter is the **expected** value the second is the **actual** value. Mixing up these two will cause confusion when investigating a test failure as the labels 'expected' and 'but was' are added to the failure message.

**DO:**
```java
Assert.assertEquals("The response id was different than expected", expectedId, response.getId());
```
**DON'T:**
```java
Assert.assertEquals("The response id was different than expected.", response.getId(), expectedId); // Inverted order.
```


### Exception

When writing negative test methods often you will need to handle exceptions and potentially validate something inside the exception. JUnit offers three options to do this, see below which one should be used:

**DO:**

```java
@Rule
public ExpectedException exception = ExpectedException.none();

@Test
public void testDispatch_WithNullRequest_ThrowsNullPointerException() throws Exception {

	// Arrange.
	this.exception.expect(NullPointerException.class);

	// Act.
	this.service.dispatch(null);

};
```

**DON'T:**

```java
@Test
public void testDispatch_WithNullRequest_ThrowsNullPointerException() throws Exception {

    // Act.
    try {
       this.service.dispatch(null);

       // Assert.
       Assert.Fail("Exception not thrown");

    catch (NullPointerException e) {
    }
}
```
```java
@Test(expected = NullPointerException.class)
public void testDispatch_WithNullRequest_ThrowsNullPointerException() throws Exception {

    // Act.
	this.service.dispatch(null);
}
```
## Guidelines

### Test Format

A unit test should have a single test responsibility, attempting to test too many aspects of the code on a single test will likely lead to unreadable and hard to maintain test methods. A typical test method will have a few lines of code setting up the inputs to be used and the unit under test, a single line calling the method under test and some lines to verify the output. This aligns with the ArrangeActAssert standard, there might be exceptions to this rule but one should only consider a different approach if the overall readability and maintainability is increased, remember that whenever doing something different one will already by breaking consistency among other tests which should only be done for the sake of readability and maintainability gain not loss.

### Mocking

Mocking should be used on the test code for two different purposes:

- Keeping the test focus on the unit under test instead of the entire chain of dependencies exercised by a given method.
- Isolating the unit under test from environment or system dependencies, i.e.: file system, database, external services, etc.

While the second reason is very clear the first one is a bit subjective. Here are some additional guidelines for when to mock:

- Mock dependencies that are behind an interface.
- Mock common dependencies that are used across different callers and have heavy business logic.
- Dependencies that are not common to multiple callers should not be mocked but tested as part of the callee unit test instead.
- Dependencies that are common but are not heavy in business logic (just an extension of the callee) should not be mocked.

See the Mocking Guide for specific cases.

#### Legacy Code

When adding unit tests to legacy code one should strive to keep the amount of changes in the code to a minimum. To help with this, we have adopted **PowerMock** which can be used to mock static dependencies without any major refactoring. One should refrain from using PowerMock to unit test any new feature, keeping the design of new features object oriented should allow unit tests to be written simply with Mockito.

Additionally, whenever unit testing legacy code and mocking dependencies ensure to add unit tests to those dependencies in isolation or track this effort accordingly.

#### New Feature Code

Any new feature code should be created already with unit tests. Remember, unit testing is not a QA phase activity but a development activity. Authoring unit tests along with the code improves code quality and enforces good patterns. To take full advantage of this side effect make sure PowerMock is not used and stick with **Mockito** only whenever mocks make sense.

### Input Variation vs. System State Manipulation

As previously mentioned, each unit test will likely need to setup a set of inputs and may depend on certain mocked behaviors. In order to keep each test method clear, refrain from setting up mocks within the body of test method. Instead focus on picking up or setting up your inputs and mock your system inside of a test initialization method (for Junit use @Before). This initialization method will be aware of the inputs the various tests within a class use and refer to them when a certain mocked behavior is needed. This approach puts all the code where the system state is set (mocked) in a single place and allows the test method to have the emphasis on the input, action and validation thus becoming more readable.

## Appendix

### Mocking Guide
| Code Under Test | Should Mock | Should NOT Mock | Existing Test Class(es) |
|--------|--------|--------|--------|
|Any service within the packages broker.service.* that implements ServiceDispatcher|   DtoValidators, Session      |*EntityMgr classes|AddDistributedApplianceServiceTest|
|Any task within the packages broker.service.tasks.* that implements TranscationalMetaTask|NsxSiRestClient or other similar clients to external services, Session|Classes within the package broker.rest.client.nsx.api|VSConformanceCheckMetaTaskTest|
