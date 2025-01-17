import { beforeEach, describe, expect, test } from '@jest/globals';
import { ChatService } from '../services/ChatService';
import { UserService } from '../services/UserService';
import { StatusType } from '../enums/StatusType';
import { BotMessageData, BotMessageService } from '../services/BotMessageService';
import { ChatHistoryService } from '../services/ChatHistoryService';
import { UserMessageService } from '../services/UserMessageService';
import { ChatItem } from '../types/ChatItem';
import { Chat } from '../types/Chat';


type ChatItemTestable = Omit<ChatItem, 'id'>;

const MOCK_CHAT: Chat = {
  chatItems: [],
  id: 'testChatId'
}

const MOCK_CHAT_ITEM: ChatItem = {
  id: 'testId',
  botMessageData: {
    text: 'testBotText',
    refetch: () => new Promise<string>(resolve => resolve('test')),
    status: StatusType.Success
  },
  userMessageData: {
    userId: 'testUserId',
    text: 'testUserText',
  }
}

const MOCK_CHAT_WITH_ITEMS: Chat = {
  ...MOCK_CHAT,
  chatItems: [MOCK_CHAT_ITEM]
}

describe('chatService', () => {
  let chatService: ChatService;
  let botMessageService: BotMessageService;
  let chatHistoryService: ChatHistoryService;
  let userMessageService: UserMessageService;
  let userService: UserService;

  beforeEach(() => {
    botMessageService = new BotMessageService();
    chatHistoryService = new ChatHistoryService();
    userService = new UserService();
    userMessageService = new UserMessageService(userService);

    chatService = new ChatService(
      botMessageService,
      chatHistoryService,
      userMessageService
    );
  })

  test('should create new chat', () => {
    const currentChat = chatService.getCurrentChat();

    expect(currentChat).toEqual(null);

    chatService.startNewChat();

    const newChat = chatService.getCurrentChat();

    expect(newChat).not.toEqual(null);
    expect(newChat?.id).not.toEqual(null);
    expect(typeof newChat?.id).toBe('string');
    expect(newChat?.chatItems.length).toBe(0);
  })

  test('should create chat item based on user query', () => {
    const TEST_QUERY = 'Test'
    const chatItem = chatService.createChatItem(TEST_QUERY);
    const { id, ...chestItemWithoutId } = chatItem;

    const expected: ChatItemTestable = {
      userMessageData: {
        userId: userService.getUserId(),
        text: TEST_QUERY,
      },
      botMessageData: {
        status: StatusType.Pending,
        text: null,
        refetch: botMessageService.simulateFetchResponse
      }
    }

    expect(id).toBeDefined();
    expect(typeof id).toBe('string');
    expect(chestItemWithoutId).toEqual(expected);
  })

  test('should add chat item', () => {
    chatService.setCurrentChat(MOCK_CHAT);

    chatService.addChatItem(MOCK_CHAT_ITEM);
    const updatedChat = chatService.getCurrentChat();

    expect(updatedChat).not.toEqual(null);
    expect(updatedChat?.chatItems).toContain(MOCK_CHAT_ITEM);
  })

  test('should throw error on add chat item', () => {
    const currentChat = chatService.getCurrentChat();

    expect(currentChat).toEqual(null);
    expect(() => chatService.addChatItem(MOCK_CHAT_ITEM)).toThrowError('Chat is not defined!');
  })

  test('should update bot message text and status', () => {

    const updatePropertyTest = <T extends keyof BotMessageData>(property: T, value: BotMessageData[T], chatItemId: string) => {
      chatService.updateBotMessageDataProperty(property, value,CHAT_ITEM_ID);

      const updatedChat = chatService.getCurrentChat();

      expect(updatedChat).not.toEqual(null);

      const foundChatItem = updatedChat?.chatItems.find((chatItem) => chatItem.id === CHAT_ITEM_ID);

      expect(foundChatItem).toBeDefined();
      expect(foundChatItem?.botMessageData[property]).toEqual(value);
    }

    const CHAT_ITEM_ID = MOCK_CHAT_WITH_ITEMS.chatItems[0].id;
    const expectedStatus = StatusType.Failed;
    const expectedText = 'Updated text!';

    chatService.setCurrentChat(MOCK_CHAT_WITH_ITEMS);
    const currentChat = chatService.getCurrentChat();

    expect(currentChat).not.toEqual(null);

    updatePropertyTest('status', expectedStatus, CHAT_ITEM_ID);
    updatePropertyTest('text', expectedText, CHAT_ITEM_ID);
  })

  test('should throw error on update bot message property when message not found', () => {
    const CHAT_ITEM_ID = MOCK_CHAT_WITH_ITEMS.chatItems[0].id;
    const expectedStatus = StatusType.Failed;

    chatService.setCurrentChat(MOCK_CHAT);
    const currentChat = chatService.getCurrentChat();
    expect(currentChat).not.toEqual(null);

    expect(() => chatService.updateBotMessageDataProperty('status', expectedStatus, CHAT_ITEM_ID)).toThrowError('Chat item with the specified id was not found in the list.');
  })

  test('should throw error on update bot message property when chat is not defined', () => {
    const CHAT_ITEM_ID = MOCK_CHAT_WITH_ITEMS.chatItems[0].id;
    const expectedStatus = StatusType.Failed;

    const currentChat = chatService.getCurrentChat();
    expect(currentChat).toEqual(null);

    expect(() => chatService.updateBotMessageDataProperty('status', expectedStatus, CHAT_ITEM_ID)).toThrowError('Chat is not defined!');
  })
})


