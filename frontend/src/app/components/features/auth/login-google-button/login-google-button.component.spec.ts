import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginGoogleButtonComponent } from './login-google-button.component';

describe('LoginGoogleButtonComponent', () => {
  let component: LoginGoogleButtonComponent;
  let fixture: ComponentFixture<LoginGoogleButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginGoogleButtonComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginGoogleButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
