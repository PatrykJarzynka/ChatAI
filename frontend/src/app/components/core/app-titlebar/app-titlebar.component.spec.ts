import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppTitlebar } from './app-titlebar.component';
import { expect, test, beforeEach, describe } from '@jest/globals';


describe('AppTitlebar', () => {
  let component: AppTitlebar;
  let fixture: ComponentFixture<AppTitlebar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppTitlebar]
    })
      .compileComponents();

    fixture = TestBed.createComponent(AppTitlebar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  test('should render content slot', () => {
    fixture.nativeElement.innerHTML = `
      <app-titlebar>
        <div class="content">Content</div>
      </app-titlebar>
    `;

    fixture.detectChanges();

    const content = fixture.nativeElement.querySelector('.content');

    expect(content).toBeTruthy();
    expect(content.textContent).toBe('Content');
  });

  test('should render provided title', () => {
    const mockTitle = 'New Title';

    fixture.componentRef.setInput('title', mockTitle);

    fixture.detectChanges();

    expect(component.title()).toBe(mockTitle);
  });
});
