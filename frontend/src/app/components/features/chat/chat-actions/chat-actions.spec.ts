import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatActions } from '../chat-actions/chat-actions.component';
import { MOCK_QUERY } from '../../../../../utils/mockedData';
import { By } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';


describe('ChatActions', () => {
  let component: ChatActions;
  let fixture: ComponentFixture<ChatActions>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ChatActions, BrowserAnimationsModule],
    });

    fixture = TestBed.createComponent(ChatActions);
    component = fixture.componentInstance;
    fixture.detectChanges();

    jest.spyOn(component, 'onUserQuerySend');
    jest.spyOn(component.querySend, 'emit');
  });


  test('should emit event on query input event call', () => {
    component.message.set(MOCK_QUERY);
    const input = fixture.nativeElement.querySelector('input');

    input.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Enter'
    }));

    expect(component.onUserQuerySend).toHaveBeenCalledWith(MOCK_QUERY);
    expect(component.querySend.emit).toHaveBeenCalledWith(MOCK_QUERY);
    expect(component.message()).toBe('');
  });

  test('should emit input event on button click', () => {
    component.message.set(MOCK_QUERY);
    const sendButton = fixture.nativeElement.querySelector('.send-button');

    sendButton.click();

    expect(component.onUserQuerySend).toHaveBeenCalledWith(MOCK_QUERY);
    expect(component.querySend.emit).toHaveBeenCalledWith(MOCK_QUERY);
    expect(component.message()).toBe('');
  });
});
