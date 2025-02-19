import { ComponentFixture, TestBed } from '@angular/core/testing';
import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { AuthView } from './auth-view.component';
import { By } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


describe('AuthView', () => {
  let component: AuthView;
  let fixture: ComponentFixture<AuthView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuthView, BrowserAnimationsModule]
    })
      .compileComponents();

    fixture = TestBed.createComponent(AuthView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  test('should change tab to register form', () => {
    const loginForm = fixture.debugElement.query(By.css('.login-form-container'));
    loginForm.componentInstance.newAccountClick.emit(loginForm);

    expect(component.selectedTabIndex()).toBe(1);
  });

  test('should change tab to login form', () => {
    jest.spyOn(component, 'onIconBackClick');
    component.selectedTabIndex.set(1);

    fixture.detectChanges();

    const goBackButton = fixture.nativeElement.querySelector('.back-button');

    goBackButton.click();
    fixture.detectChanges();

    expect(component.onIconBackClick).toHaveBeenCalled();
    expect(component.selectedTabIndex()).toBe(0);
  });
});
