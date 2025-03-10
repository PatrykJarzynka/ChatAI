import { AuthProvider } from '@appTypes/AuthProvider';


export interface UserRegisterData {
  email: string;
  password: string;
  fullName: string;
  tenant: AuthProvider;
}
