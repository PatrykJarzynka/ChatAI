import { Injectable, signal } from '@angular/core';
import { ApiService } from '@services/ApiService';
import { UserModel } from '@models/UserModel';


const ENDPOINT = 'user';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private user = signal<UserModel | null>(null);

  constructor(private apiService: ApiService) {
  }

  getCurrentUser() {
    return this.user;
  }

  setCurrentUser(user: UserModel) {
    this.user.set(user);
  }

  async fetchUser(): Promise<UserModel> {
    return await this.apiService.get<UserModel>(`${ ENDPOINT }/me`);
  }

  async createOrUpdateGoogleUser(): Promise<void> {
    await this.apiService.post<void, {}>(`${ ENDPOINT }/google`, Object);
  }

  async createOrUpdateMicrosoftUser(): Promise<void> {
    await this.apiService.post<void, {}>(`${ ENDPOINT }/microsoft`, Object);
  }
}
