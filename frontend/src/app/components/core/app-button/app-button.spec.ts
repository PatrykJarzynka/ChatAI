import { beforeEach, describe, expect, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppButton } from '../../../components/core/app-button/app-button.component';
import { MatTooltip, MatTooltipModule } from '@angular/material/tooltip';
import { By } from '@angular/platform-browser';


describe('AppButton', () => {
  let component: AppButton;
  let fixture: ComponentFixture<AppButton>;
  let expectedLabel: string;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppButton, MatTooltipModule],
      providers: [MatTooltip]
    });

    fixture = TestBed.createComponent(AppButton);
    component = fixture.componentInstance;

    expectedLabel = 'Click me';
  });

  test('should display label provided with input', () => {
    fixture.componentRef.setInput('label', expectedLabel);
    fixture.detectChanges();

    const buttonElement: HTMLButtonElement = fixture.nativeElement.querySelector('button');
    expect(buttonElement.textContent).toContain(expectedLabel);
  });

  test('should contain icon button class', () => {
    fixture.componentRef.setInput('iconMode', true);
    fixture.detectChanges();

    const buttonElement: HTMLButtonElement = fixture.nativeElement.querySelector('button');
    expect(buttonElement.classList.contains('icon-button')).toBe(true);
  });

  test('should not contain icon button class', () => {
    fixture.componentRef.setInput('iconMode', false);
    fixture.detectChanges();

    const buttonElement: HTMLButtonElement = fixture.nativeElement.querySelector('button');
    expect(buttonElement.classList.contains('icon-button')).toBe(false);
  });

  test('should display tooltip message provided with input', async () => {
    const TOOLTIP_CONTENT = 'Hello';
    fixture.componentRef.setInput('tooltip', TOOLTIP_CONTENT);
    fixture.detectChanges();

    const tooltipDirective = fixture.debugElement.query(By.css('button')).injector.get(MatTooltip);

    expect(tooltipDirective.message).toBe(TOOLTIP_CONTENT);
  });

  test('should not display tooltip message when tooltip input is not provided', () => {
    const tooltipDirective = fixture.debugElement.query(By.css('button')).injector.get(MatTooltip);

    tooltipDirective.show();
    fixture.detectChanges();


    expect(tooltipDirective._isTooltipVisible()).toBe(false);
  });
});
