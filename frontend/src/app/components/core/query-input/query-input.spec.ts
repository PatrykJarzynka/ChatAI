import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { QueryInput } from './query-input.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';


describe('QueryInput', () => {
  let component: QueryInput;
  let fixture: ComponentFixture<QueryInput>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [QueryInput, BrowserAnimationsModule, MatIconModule],
    });

    fixture = TestBed.createComponent(QueryInput);
    component = fixture.componentInstance;
  });

  test('should set new query', () => {
    const mockQuery = 'Hello there.';

    fixture.componentRef.setInput('query', mockQuery);

    fixture.detectChanges();

    expect(component.query()).toBe(mockQuery);
  });

  test('should set new placeholder', () => {
    const mockPlaceholder = 'Placeholder test.';

    fixture.componentRef.setInput('placeholder', mockPlaceholder);

    fixture.detectChanges();

    expect(component.placeholder()).toBe(mockPlaceholder);
  });

  test('should emit event on enterPressed', () => {
    jest.spyOn(component, 'onEnter');
    component.enterPressed.emit = jest.fn();

    fixture.detectChanges();

    const inputElement = fixture.nativeElement.querySelector('input');
    inputElement.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Enter'
    }));

    expect(component.onEnter).toHaveBeenCalled();
    expect(component.enterPressed.emit).toHaveBeenCalled();
  });

  test('should render provided suffix', () => {
    fixture.nativeElement.innerHTML = `
      <query-input>
        <div suffix class="suffix">Test</div>
      </query-input>
    `;

    fixture.detectChanges();

    const suffix = fixture.nativeElement.querySelector('.suffix');

    expect(suffix).toBeTruthy();
    expect(suffix.textContent).toBe('Test');
  });

  test('should render provided prefix', () => {
    fixture.nativeElement.innerHTML = `
      <query-input>
        <div prefix class="prefix">Test</div>
      </query-input>
    `;

    fixture.detectChanges();

    const prefix = fixture.nativeElement.querySelector('.prefix');

    expect(prefix).toBeTruthy();
    expect(prefix.textContent).toBe('Test');
  });

});
