import { Component, output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatIconButton } from '@angular/material/button';


@Component({
  selector: 'register-form',
  imports: [MatIconModule, MatIconButton],
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.scss'
})
export class RegisterForm {
  constructor() {
  }

  iconBackClick = output<void>();

  onIconBackClick(): void {
    this.iconBackClick.emit();
  }
}
