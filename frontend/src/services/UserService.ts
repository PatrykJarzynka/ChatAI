import { Injectable } from '@angular/core';
import { USER_ID } from '../constants';


@Injectable({
  providedIn: 'root'
})
export class UserService {
  private id = USER_ID;

  constructor() {
  }

  getUserId() {
    return this.id;
  }
}
