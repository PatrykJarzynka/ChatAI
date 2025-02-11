import { Component, model, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'query-input',
  templateUrl: 'query-input.component.html',
  styleUrl: 'query-input.component.scss',
  imports: [FormsModule, MatFormFieldModule, MatIconModule, MatInputModule, MatButtonModule],
  standalone: true,
})

export class QueryInput {
  query = model<string>('');

  enterPressed = output<void>();

  onEnter() {
    this.enterPressed.emit();
  }
}
