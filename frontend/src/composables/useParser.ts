import { ChatResponse } from '../models/ChatResponse';
import { Chat } from '../types/Chat';
import { StatusType } from '../enums/StatusType';
import { camelCase, isObject, snakeCase } from 'lodash';


type CaseType = 'camel' | 'snake'

function useParser() {
  function parseChatResponseToChat(chatResponse: ChatResponse): Chat {
    return {
      id: chatResponse.id,
      chatItems: chatResponse.chatItems.map(item => ( {
        userMessage: item.userMessage,
        botMessageData: {
          text: item.botMessage,
          status: StatusType.Success
        }
      } ))
    };
  }

  function parseArrayOfObjectsIntoMap<T, K extends keyof T>(array: T[], key: K): Map<T[K], T> {
    return new Map(array.map(item => [item[key], item]));
  }

  function convertObjectsKeysCase<T>(input: T, caseType: CaseType): T {
    const caseConverter = caseType === 'camel'
      ? camelCase
      : snakeCase;

    if (Array.isArray(input)) {
      return input.map((value) => convertObjectsKeysCase(value, caseType)) as T;
    }
    if (isObject(input) && !Array.isArray(input)) {
      return Object.keys(input).reduce((acc, key) => {
        const newKey = caseConverter(key);
        const value = ( input as any )[key];

        ( acc as any )[newKey] = isObject(value) || Array.isArray(value)
          ? convertObjectsKeysCase(value, caseType)
          : value;

        return acc;
      }, {} as T);
    }
    return input;
  }

  return {
    parseChatResponseToChat,
    parseArrayOfObjectsIntoMap,
    convertObjectsKeysCase
  };
}

export default useParser();
