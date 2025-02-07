import { Component, input, output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatDivider } from '@angular/material/divider';
import { MatMiniFabButton } from '@angular/material/button';
import { MatTooltip } from '@angular/material/tooltip';


@Component({
  selector: 'app-sidebar',
  imports: [MatIconModule, MatDivider, MatMiniFabButton, MatTooltip],
  templateUrl: './app-sidebar.component.html',
  styleUrl: './app-sidebar.component.scss',
  standalone: true,
})
export class AppSidebar {

  panelVisibilityIconClick = output<void>();
  title = input<string>();

  constructor() {
  }
}
