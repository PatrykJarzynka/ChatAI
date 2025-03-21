import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginMicrosoftButtonComponent } from './login-microsoft-button.component';

describe('LoginMicrosoftButtonComponent', () => {
  let component: LoginMicrosoftButtonComponent;
  let fixture: ComponentFixture<LoginMicrosoftButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginMicrosoftButtonComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginMicrosoftButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
