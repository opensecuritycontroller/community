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

For details on Arrange-Act-Assert, see the Test Format session below. 

Add the comments **// Arrange. // Act. // Assert**. within the body of your test method to create clear, visual boundaries. Making this step a core part of the test helps to both organize the code and facilitate code reviews by providing a better picture as to exactly what is being setup and how it is being validated. This is particularly useful for test methods with several arrange and assert lines. These comments may not be necessary for short test methods. 

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

To validate test results, use the methods offered by org.junit.Assert. Observe that most of the assertion methods have an overloaded flavor that requires a String to be used as a message when the assertion fails. ALWAYS use this version of the method. An error message displays when the test fails, helping to quickly identify the source of the error. 

 >Note: Asserts within the same test method should never have the same message.

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

When writing negative test methods, you must handle exceptions, along with the potential validation of something within the exception. JUnit offers three of the following options:

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

A unit test should have a single test responsibility. Attempting to test too many aspects of the code on a single test will likely lead to unreadable and test methods that are difficult to maintain. A typical test method contains a few lines of code to set up the inputs used along with the unit under test, a single line calling the method under test, and some lines to verify the output. This aligns with the ArrangeActAssert standard however, there might be exceptions to this rule. Only consider a different approach if the overall readability and maintainability is increased.  For consistency, it is important to remember that other tests should be completed only for the sake of readability and to maintain gain, not loss.  

### Mocking

Mocking should be used on the test code for two different purposes: 

- To keep the test focus on the unit under test, rather than the entire chain of dependencies exercised by a given method.
- To isolate the unit under test from environment or system dependencies, i.e.: file system, database, external services, etc.

While the second reason is clear, the first is a bit subjective. Follow these additional guidelines for when to mock:

- Mock dependencies that are behind an interface.
- Mock common dependencies used across different callers that contain heavy business logic.
- Dependencies uncommon to multiple callers should be tested as part of the callee unit test rather than mocked.
- Dependencies that are common but not heavy in business logic (just an extension of the callee) should not be mocked.

See the Mocking Guide for specific cases.

#### Legacy Code

When adding unit tests to legacy code, you should strive to keep the amount of changes in the code to a minimum. PowerMock is able to help and can be used to mock static dependencies without any major refactoring. Refrain from using **PowerMock** to unit test new features, as keeping their designs object-oriented should allow unit tests to be written with **Mockito**.

Additionally, when unit testing legacy code and mocking dependencies, ensure you add unit tests to dependencies in isolation or track this effort accordingly.

#### New Feature Code

Any new feature code should already be created with unit tests. Remember, unit testing is a development activity rather than a QA phase activity. Authoring unit tests along with the code improves code quality and enforces good patterns. To take full advantage of this side effect, make sure PowerMock is not used. Stick with **Mockito** only whenever mocks make sense.

### Input Variation vs. System State Manipulation

As previously mentioned, each unit test will likely need to setup a set of inputs and may depend on certain mocked behaviors. To keep each test method clear, refrain from setting up mocks within the body of test method. Instead, focus on picking up or setting up your inputs and, mocking your system inside of a test initialization method (for Junit use @Before). This initialization method is aware of inputs that the various tests within a class use, and refers to them when a certain mocked behavior is needed. This approach places all the code where the system state is set (mocked) in a single place, allowing the test method to have emphasis on the input, action and validation, while creating more readability.

## Appendix

### Mocking Guide
| Code Under Test | Should Mock | Should NOT Mock | Existing Test Class(es) |
|--------|--------|--------|--------|
|Any service within the packages broker.service.* that implements ServiceDispatcher|   DtoValidators, Session      |*EntityMgr classes|AddDistributedApplianceServiceTest|
|Any task within the packages broker.service.tasks.* that implements TranscationalMetaTask|NsxSiRestClient or other similar clients to external services, Session|Classes within the package broker.rest.client.nsx.api|VSConformanceCheckMetaTaskTest|
