import { Component, input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-button',
  imports: [MatIconModule],
  templateUrl: './app-button.component.html',
  styleUrl: './app-button.component.scss',
  standalone: true,
})
export class AppButton {
  label = input<string>();
}
