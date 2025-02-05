import { Component, model, output } from '@angular/core';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'query-input',
  templateUrl: 'query-input.component.html',
  styleUrl: 'query-input.component.scss',
  imports: [FormsModule],
  standalone: true,
})

export class QueryInput {
  query = model<string>('');

  enterPressed = output<void>();

  onEnter() {
    this.enterPressed.emit();
  }
}
