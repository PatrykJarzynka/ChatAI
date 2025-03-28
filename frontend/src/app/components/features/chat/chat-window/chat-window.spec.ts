import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChatWindow } from '../chat-window/chat-window.component';
import { MOCK_CHAT_WITH_ITEMS } from '@utils/mockedData';
import { ChatService } from '@services/ChatService';
import { StatusType } from '@enums/StatusType';


describe('ChatWindow', () => {
  let component: ChatWindow;
  let fixture: ComponentFixture<ChatWindow>;
  let chatService: ChatService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ChatWindow],
    });

    fixture = TestBed.createComponent(ChatWindow);
    chatService = TestBed.inject(ChatService);

    component = fixture.componentInstance;

    fixture.detectChanges();
  });


  test('should display default text when no chat is set', () => {
    const initialMessage = fixture.nativeElement.querySelector('.initial-message');
    expect(initialMessage.textContent).toEqual('How can I help you today?');
  });

  test('should display one chat item', () => {
    chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

    fixture.detectChanges();

    const chatItem = fixture.nativeElement.querySelector('.chat-grid-item');
    const userMessage = chatItem.querySelector('.chat-message');
    const responseLoader = chatItem.querySelector('.loader-wrapper');

    expect(userMessage.textContent).toEqual(MOCK_CHAT_WITH_ITEMS.chatItems[0].userMessage);
    expect(responseLoader).toBeTruthy();
  });

  test('should change response loader to text', () => {
    const MOCK_RESPONSE = 'Text response';
    chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);
    fixture.detectChanges();

    chatService.updateLatestBotMessageDataProperty('text', MOCK_RESPONSE);
    chatService.updateLatestBotMessageDataProperty('status', StatusType.Success);

    fixture.detectChanges();

    const messageResponse = fixture.nativeElement.querySelector('.chat-message--response');

    expect(messageResponse.textContent).toEqual(MOCK_RESPONSE);
  });

  test('should change response loader to failed text and render refetch button', () => {
    chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);
    fixture.detectChanges();

    chatService.updateLatestBotMessageDataProperty('status', StatusType.Failed);

    fixture.detectChanges();

    const messageResponse = fixture.nativeElement.querySelector('.chat-message--response');
    const errorButton = fixture.nativeElement.querySelector('.error-button');
    const errorButtonLabel = errorButton.querySelector('.button-label');
    const errorButtonIcon = errorButton.querySelector('.mat-icon');

    expect(messageResponse.textContent).toEqual('Something went wrong while fetching chat response...');
    expect(errorButtonLabel.textContent).toEqual('Try again');
    expect(errorButtonIcon.textContent).toEqual('rotate_right');
  });

  test('should emit refetch event after refetch button click', () => {
    jest.spyOn(component.refreshButtonClick, 'emit');
    chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);
    fixture.detectChanges();

    chatService.updateLatestBotMessageDataProperty('status', StatusType.Failed);

    fixture.detectChanges();

    const refetchButton = fixture.nativeElement.querySelector('.error-button');
    refetchButton.click();

    expect(component.refreshButtonClick.emit).toHaveBeenCalledWith(MOCK_CHAT_WITH_ITEMS.chatItems[0].userMessage);
  });

});
