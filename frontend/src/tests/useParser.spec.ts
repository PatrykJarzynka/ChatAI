import { describe, expect, test } from '@jest/globals';
import useParser from '@composables/useParser';
import { ValidationErrors } from '@angular/forms';


const { convertObjectsKeysCase, parseValidationErrorToString } = useParser;

const MOCK_DATA = {
  testOne: 1,
  test_two: 2,
  'test-Three': 3,
  '!TEST-four': 4,
  '!test-FIVE?': 5,
  test7: {
    test_eight: 8,
    testNine: 9
  }
};

const MOCK_DATA_ARRAY = [
  {
    testOne: 1,
    test_two: 2,
  },
  {
    'test-Three': 3,
    '!TEST-four': 4,
  },
  {
    '!test-FIVE?': 5,
    test7: {
      test_eight: 8,
      testNine: 9
    }
  }
];

const MOCK_INPUTS = [
  {
    input: 123,
    expected_snake: 123,
    expected_camel: 123,
  },
  {
    input: 'teSt',
    expected_snake: 'teSt',
    expected_camel: 'teSt',
  },
  {
    input: null,
    expected_snake: null,
    expected_camel: null,
  },
  {
    input: {},
    expected_snake: {},
    expected_camel: {},
  },
  {
    input: undefined,
    expected_snake: undefined,
    expected_camel: undefined,
  },
  {
    input: MOCK_DATA,
    expected_snake: {
      test_one: 1,
      test_two: 2,
      test_three: 3,
      test_four: 4,
      test_five: 5,
      test_7: {
        test_eight: 8,
        test_nine: 9
      }
    },
    expected_camel: {
      testOne: 1,
      testTwo: 2,
      testThree: 3,
      testFour: 4,
      testFive: 5,
      test7: {
        testEight: 8,
        testNine: 9
      }
    }
  },
  {
    input: MOCK_DATA_ARRAY,
    expected_snake: [
      {
        test_one: 1,
        test_two: 2,
      },
      {
        test_three: 3,
        test_four: 4,
      },
      {
        test_five: 5,
        test_7: {
          test_eight: 8,
          test_nine: 9
        }
      }
    ],
    expected_camel: [
      {
        testOne: 1,
        testTwo: 2,
      },
      {
        testThree: 3,
        testFour: 4,
      },
      {
        testFive: 5,
        test7: {
          testEight: 8,
          testNine: 9
        }
      }
    ],
  }
];

describe('useParser', () => {

  describe('parseRequestToSnakeCase', () => {
    test('should parse objects keys to snake case', () => {
      MOCK_INPUTS.forEach(inputData => {
        expect(convertObjectsKeysCase(inputData.input, 'snake')).toEqual(inputData.expected_snake);
      });
    });
  });

  describe('parseResponseToCamelCase', () => {
    test('should parse object keys to camel case', () => {
      MOCK_INPUTS.forEach(inputData => {
        expect(convertObjectsKeysCase(inputData.input, 'camel')).toEqual(inputData.expected_camel);
      });
    });
  });

  describe('parseValidationErrorToString', () => {
    test('should parse ValidationErrors to string', () => {

      interface TestCase {
        error: ValidationErrors | null,
        expected: string | null,
      }

      const testCases: TestCase[] = [
        {
          error: { required: true },
          expected: 'This field is required'
        },
        {
          error: { email: true },
          expected: 'Incorrect email address'
        },
        {
          error: { comparePassword: true },
          expected: 'Passwords do not match'
        },
        {
          error: { emailExists: true },
          expected: 'This email already exists'
        },
        {
          error: { credentials: true },
          expected: 'Incorrect email or password'
        },
        {
          error: { someKey: true },
          expected: 'Incorrect field'
        },
        {
          error: null,
          expected: null
        }
      ];

      testCases.forEach(testCase => {
        expect(parseValidationErrorToString(testCase.error)).toEqual(testCase.expected);
      });
    });
  });
});
