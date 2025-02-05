export interface ChatResponse {
  chatItems: {
    userMessage: string;
    botMessage: string;
  }[],
  id: number;
}
