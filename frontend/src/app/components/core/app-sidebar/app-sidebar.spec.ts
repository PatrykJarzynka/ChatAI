import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AppSidebar } from '../app-sidebar/app-sidebar.component';


describe('ResizablePanel', () => {
  let component: AppSidebar;
  let fixture: ComponentFixture<AppSidebar>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppSidebar],
    });

    fixture = TestBed.createComponent(AppSidebar);

    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  test('should render multiple slots with ng-content select', () => {
    fixture.nativeElement.innerHTML = `
      <app-component>
        <div panel-actions class="actions-content">Actions Content</div>
        <div panel-content class="panel-content">Panel Content</div>
      </app-component>
    `;

    fixture.detectChanges();

    const actions = fixture.nativeElement.querySelector('.actions-content');
    const content = fixture.nativeElement.querySelector('.panel-content');

    expect(actions).toBeTruthy();
    expect(actions.textContent).toBe('Actions Content');

    expect(content).toBeTruthy();
    expect(content.textContent).toBe('Panel Content');
  });

  test('should emit event after button click', () => {
    jest.spyOn(component.panelVisibilityIconClick, 'emit');
    const sidebarButton = fixture.nativeElement.querySelector('.app-sidebar-toggle-button');

    sidebarButton.click();

    expect(component.panelVisibilityIconClick.emit).toHaveBeenCalled();
  });
});
