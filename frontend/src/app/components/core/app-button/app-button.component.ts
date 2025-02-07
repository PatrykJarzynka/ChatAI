import { Component, input } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltip } from '@angular/material/tooltip';


@Component({
  selector: 'app-button',
  imports: [MatIconModule, MatTooltip],
  templateUrl: './app-button.component.html',
  styleUrl: './app-button.component.scss',
  standalone: true,
})
export class AppButton {
  type = input<'mini-icon' | 'icon' | 'icon-labeled' | 'text'>();
  icon = input<string>();

  label = input<string>();
  iconMode = input<boolean>();
  tooltip = input<string>();
}
