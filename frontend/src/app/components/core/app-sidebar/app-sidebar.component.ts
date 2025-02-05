import { Component, output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { AppButton } from '../app-button/app-button.component';


@Component({
  selector: 'app-sidebar',
  imports: [MatIconModule, AppButton],
  templateUrl: './app-sidebar.component.html',
  styleUrl: './app-sidebar.component.scss',
  standalone: true,
})
export class AppSidebar {

  panelVisibilityIconClick = output<void>();

  constructor() {
  }
}
