import { Component, input } from '@angular/core';


@Component({
  selector: 'app-titlebar',
  imports: [],
  templateUrl: './app-titlebar.component.html',
  styleUrl: './app-titlebar.component.scss'
})
export class AppTitlebar {

  title = input<string>();

}
