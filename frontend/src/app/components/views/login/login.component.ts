import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { QueryInput } from '../../core/query-input/query-input.component';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'login-view',
  imports: [MatCardModule, QueryInput, MatButtonModule, MatIconModule, MatButtonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginView {

}
