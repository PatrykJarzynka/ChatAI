import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AppTitlebarComponent } from './app-titlebar.component';

describe('AppTitlebarComponent', () => {
  let component: AppTitlebarComponent;
  let fixture: ComponentFixture<AppTitlebarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppTitlebarComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AppTitlebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
