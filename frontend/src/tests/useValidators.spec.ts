import { describe, expect, test } from '@jest/globals';
import useValidators from '@composables/useValidators';
import { FormControl, FormGroup } from '@angular/forms';


const { validateSamePassword } = useValidators;

describe('useValidators', () => {
  describe('validateSamePassword', () => {

    test('should set error on confirmPassword field', () => {
      const mockedForm = new FormGroup({
        password: new FormControl('mockPassword'),
        confirmPassword: new FormControl('mockPassword1'),
      });

      expect(validateSamePassword(mockedForm)).toEqual({ comparePassword: true });
      expect(mockedForm.controls['confirmPassword'].errors).toEqual({ comparePassword: true });
      expect(mockedForm.invalid).toBe(true);
    });

    test('should be valid form', () => {
      const mockedForm = new FormGroup({
        password: new FormControl('mockPassword'),
        confirmPassword: new FormControl('mockPassword'),
      });

      expect(mockedForm.controls['confirmPassword'].errors).toEqual(null);
      expect(validateSamePassword(mockedForm)).toEqual(null);
      expect(mockedForm.valid).toBe(true);
    });


  });
});
