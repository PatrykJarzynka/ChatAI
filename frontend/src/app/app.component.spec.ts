import { beforeEach, describe, expect, jest, test } from '@jest/globals';
import { AppComponent } from './app.component';
import { ChatService } from '../services/ChatService';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MOCK_CHAT_HISTORY, MOCK_CHAT_WITH_ITEMS, MOCK_QUERY, MOCKED_INITIAL_CHAT } from '../utils/mockedData';
import { ChatActions } from '../app/components/features/chat/chat-actions/chat-actions.component';
import { By } from '@angular/platform-browser';
import { ChatHistoryService } from '../services/ChatHistoryService';
import useChatActions from '../composables/useChatActions';
import { Chat } from '../types/Chat';
import { StatusType } from '../enums/StatusType';
import { AppSidebar } from '../app/components/core/app-sidebar/app-sidebar.component';


jest.mock('../composables/useChatActions', () => (
  jest.fn(() => ( {
    handleFetchingBotMessage: jest.fn(),
  } ))
));

describe('appComponent', () => {
  let appComponent: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let chatService: ChatService;
  let chatHistoryService: ChatHistoryService;
  let mockHandleFetchingBotMessage: jest.Mock;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [AppComponent, AppSidebar, ChatActions],
      providers: [ChatService],
    });

    chatService = TestBed.inject(ChatService);
    chatHistoryService = TestBed.inject(ChatHistoryService);
    jest.spyOn(chatHistoryService, 'fetchChatHistories').mockResolvedValue([MOCK_CHAT_HISTORY]);
    mockHandleFetchingBotMessage = jest.fn();
    ( useChatActions as jest.Mock ).mockReturnValue({
      handleFetchingBotMessage: mockHandleFetchingBotMessage,
    });


    fixture = TestBed.createComponent(AppComponent);
    appComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  describe('togglePanelVisibility', () => {
    test('should toggle panel visibility when panel emits toggle event', async () => {
      const panelButton = fixture.nativeElement.querySelector('.app-sidebar-toggle-button');
      panelButton.click();

      fixture.detectChanges();

      await fixture.whenStable();

      expect(appComponent.panelVisibility()).toEqual(false);
    });
  });

  describe('startNewChat', () => {
    let panel: HTMLDivElement;
    let panelNewChatButton: HTMLButtonElement | null;

    beforeEach(() => {
      jest.spyOn(appComponent, 'startNewChat');
      jest.spyOn(chatService, 'startNewChat');

      panel = fixture.nativeElement.querySelector('.sidebar-wrapper');
      panelNewChatButton = panel.querySelector('.new-chat-button');
    });

    test('should start new chat when panel emits new chat event', async () => {
      jest.spyOn(chatService, 'fetchNewChat').mockResolvedValue(MOCK_CHAT_WITH_ITEMS);
      chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);

      if (panelNewChatButton) {
        panelNewChatButton.click();
      }

      expect(appComponent.startNewChat).toHaveBeenCalled();
      expect(chatService.startNewChat).toHaveBeenCalled();
    });

    test('should not start new chat when panel emits new chat event', async () => {
      chatService.setCurrentChat(MOCKED_INITIAL_CHAT);

      if (panelNewChatButton) {
        panelNewChatButton.click();
      }

      expect(appComponent.startNewChat).toHaveBeenCalled();
      expect(chatService.startNewChat).not.toHaveBeenCalled();
    });
  });

  describe('onUserQuerySend', () => {

    beforeEach(() => {
      jest.spyOn(appComponent, 'onUserQuerySend');
      jest.spyOn(chatService, 'startNewChat');
      jest.spyOn(chatService, 'createAndAddChatItemTemplate');
      jest.spyOn(chatService, 'fetchNewChat').mockResolvedValue(MOCKED_INITIAL_CHAT);
    });

    test('should create new chat, create chat item and update bot message on chat action button click', async () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      const chatActionsButton = chatActions.nativeElement.querySelector('.app-button');

      chatActions.componentInstance.message.set(MOCK_QUERY);

      chatActionsButton.click();

      await fixture.whenStable();
      expect(appComponent.onUserQuerySend).toHaveBeenCalledWith(MOCK_QUERY);
      expect(chatService.startNewChat).toHaveBeenCalled();
      await fixture.whenStable();
      expect(chatService.createAndAddChatItemTemplate).toHaveBeenCalledWith(MOCK_QUERY);
      expect(mockHandleFetchingBotMessage).toHaveBeenCalledWith(MOCK_QUERY, appComponent.shouldFail());
    });

    test('should create new chat, create chat item and update bot message on chat action enter key press', async () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      const chatActionsQueryInput = chatActions.nativeElement.querySelector('.query-input');

      chatActions.componentInstance.message.set(MOCK_QUERY);

      chatActionsQueryInput.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Enter'
      }));

      await fixture.whenStable();
      expect(appComponent.onUserQuerySend).toHaveBeenCalledWith(MOCK_QUERY);
      expect(chatService.startNewChat).toHaveBeenCalled();
      await fixture.whenStable();
      expect(chatService.createAndAddChatItemTemplate).toHaveBeenCalledWith(MOCK_QUERY);
      expect(mockHandleFetchingBotMessage).toHaveBeenCalledWith(MOCK_QUERY, appComponent.shouldFail());
    });

    test('should not react on enter key press', () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      const chatActionsQueryInput = chatActions.nativeElement.querySelector('.query-input');

      chatActionsQueryInput.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Enter'
      }));

      expect(appComponent.onUserQuerySend).not.toHaveBeenCalled();
    });

    test('should not react on button click', () => {
      const chatActions = fixture.debugElement.query(By.css('.chat-actions'));
      const chatActionsButton = chatActions.nativeElement.querySelector('.app-button');

      chatActionsButton.click();

      expect(appComponent.onUserQuerySend).not.toHaveBeenCalled();
    });
  });

  describe('refetchBotMessage', () => {
    test('should refetch bot message', () => {
      jest.spyOn(appComponent, 'refetchBotMessage');
      jest.spyOn(chatService, 'updateLatestBotMessageDataProperty');

      const MOCK_CHAT_WITH_FAILED_BOT_MESSAGE: Chat = {
        id: 123,
        chatItems: [
          {
            userMessage: MOCK_QUERY,
            botMessageData: {
              text: 'Test',
              status: StatusType.Failed
            }
          }
        ]
      };

      chatService.setCurrentChat(MOCK_CHAT_WITH_FAILED_BOT_MESSAGE);
      const chatWindow = fixture.nativeElement.querySelector('.chat-window');
      fixture.detectChanges();
      const chatItemRefreshButton = chatWindow.querySelector('.app-button');

      chatItemRefreshButton.click();

      expect(appComponent.refetchBotMessage).toHaveBeenCalledWith(MOCK_QUERY);
      expect(chatService.updateLatestBotMessageDataProperty).toHaveBeenCalledWith('status', StatusType.Pending);
      expect(mockHandleFetchingBotMessage).toHaveBeenCalledWith(MOCK_QUERY, appComponent.shouldFail());

    });
  });


});
