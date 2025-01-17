import { Injectable } from '@angular/core';
import { UserService } from '../services/UserService';

export interface UserMessageData {
  userId: string;
  text: string;
}

@Injectable({
  providedIn: 'root',
})
export class UserMessageService {
  constructor(private userService: UserService) {}

  createMessageData(userQuery: string): UserMessageData {
    return {
      userId: this.userService.getUserId(),
      text: userQuery,
    }
  }
}
