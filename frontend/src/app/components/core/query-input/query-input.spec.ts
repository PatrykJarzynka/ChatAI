import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { QueryInput } from '../../../components/core/query-input/query-input.component';


describe('QueryInput', () => {
  let component: QueryInput;
  let fixture: ComponentFixture<QueryInput>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [QueryInput],
    });

    fixture = TestBed.createComponent(QueryInput);
    component = fixture.componentInstance;
  });

  test('should set new query', () => {
    fixture.componentRef.setInput('query', 'Hello there.');

    fixture.detectChanges();

    expect(component.query()).toBe('Hello there.');
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

});
