import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatActions } from '../chat-actions/chat-actions.component';
import { MOCK_QUERY } from '../../../../../utils/mockedData';


describe('ChatActions', () => {
  let component: ChatActions;
  let fixture: ComponentFixture<ChatActions>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ChatActions],
    });

    fixture = TestBed.createComponent(ChatActions);
    component = fixture.componentInstance;

    jest.spyOn(component, 'onUserQuerySend');
    jest.spyOn(component.querySend, 'emit');
    component.message.set(MOCK_QUERY);
  });


  test('should emit event on query input enter and clear message state', () => {
    const chatActionsQueryInput = fixture.nativeElement.querySelector('input');

    chatActionsQueryInput.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Enter'
    }));

    expect(component.onUserQuerySend).toHaveBeenCalledWith(MOCK_QUERY);
    expect(component.querySend.emit).toHaveBeenCalledWith(MOCK_QUERY);
    expect(component.message()).toBe(null);
  });
});
