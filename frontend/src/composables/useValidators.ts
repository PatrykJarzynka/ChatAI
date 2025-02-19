import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';


function useValidators() {
  const validateSamePassword = (control: AbstractControl): ValidationErrors | null => {
    const passwordControl = control.get('password');
    const confirmPasswordControl = control.get('confirmPassword');

    if (passwordControl?.value !== confirmPasswordControl?.value) {
      const error = { comparePassword: true };
      confirmPasswordControl?.setErrors(error);
      return error;
    }
    return null;
  };


  return {
    validateSamePassword
  };
}

export default useValidators();
