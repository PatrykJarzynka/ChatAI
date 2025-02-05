import { StatusType } from '../enums/StatusType';
import { ChatService } from '../services/ChatService';


function useChatActions(chatService: ChatService) {

  async function handleFetchingBotMessage(userQuery: string, shouldFail: boolean): Promise<void> {
    const currentChat = chatService.getCurrentChat();

    if (!currentChat) {
      throw new Error('Chat is not defined!');
    } else {
      try {
        const response = await chatService.fetchBotResponse(userQuery, currentChat.id, shouldFail);

        chatService.updateLatestBotMessageDataProperty('text', response);
        chatService.updateLatestBotMessageDataProperty('status', StatusType.Success);
        chatService.updateChatHistory();
      } catch (error) {
        chatService.updateLatestBotMessageDataProperty('status', StatusType.Failed);
      }
    }
  }

  return {
    handleFetchingBotMessage
  };
}

export default useChatActions;
