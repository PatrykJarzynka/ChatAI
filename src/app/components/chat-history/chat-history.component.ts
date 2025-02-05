import { Component } from '@angular/core';
import { ChatHistoryService } from '../../../services/ChatHistoryService';
import { Chat } from '../../../types/Chat';
import { StatusType } from '../../../enums/StatusType';
import { ChatService } from '../../../services/ChatService';


@Component({
  selector: 'chat-history',
  imports: [],
  templateUrl: './chat-history.component.html',
  styleUrl: './chat-history.component.scss'
})
export class ChatHistory {
  mockHistory: Chat[] = [
    {
      id: '1',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '2',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    },
    {
      id: '3',
      chatItems: [
        {
          id: '1',
          userMessageData: {
            text: 'Test1',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '2',
          userMessageData: {
            text: 'Test2',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        },
        {
          id: '3',
          userMessageData: {
            text: 'Test3',
            userId: 'user1'
          },
          botMessageData: {
            text: 'Mock message',
            status: StatusType.Success,
            refetch: () => new Promise((resolve) => setTimeout(resolve, 1000))
          }
        }
      ]
    }
  ]

  chatHistories = () => this.chatHistoryService.getAllChatHistories().values();
  // chatHistories = this.mockHistory

  constructor(
    private chatHistoryService: ChatHistoryService,
    private chatService: ChatService
  ) {}

  updateCurrentChat(chatId: string) {
    const chat = this.chatHistoryService.getChatHistoryByChatId(chatId);

    if (chat) {
      this.chatService.setCurrentChat(chat);
    }
  }

  protected readonly JSON = JSON;
}
