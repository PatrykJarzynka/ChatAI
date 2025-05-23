import { StatusType } from '@enums/StatusType';
import { ChatService } from '@services/ChatService';
import { UserService } from '@services/UserService';
import { FileManager } from '@services/FileMananger';


function useChatActions(chatService: ChatService, userService: UserService, fileManager: FileManager) {

  async function handleFetchingBotMessage(userQuery: string): Promise<void> {
    const currentChat = chatService.getCurrentChat();
    const currentUserId = userService.getCurrentUser()()?.id;
    const selectedFilesIds = [...fileManager.getSelectedFilesIds()()];

    if (!currentChat) {
      throw new Error('Chat is not defined!');
    } else if (!currentUserId) {
      throw new Error('User is not defined!');
    } else {
      try {
        const response = await chatService.fetchBotResponse(userQuery, currentChat.id, currentUserId, selectedFilesIds);
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
