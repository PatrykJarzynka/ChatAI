import { Routes } from '@angular/router';
import { AuthView } from '@components/views/auth-view/auth-view.component';
import { ChatView } from '@components/views/chat-view/chat-view.component';
import { AuthCallback } from '@components/views/auth-callback/auth-callback.component';


export const routes: Routes = [
  { path: '', component: AuthView },
  { path: 'chat', component: ChatView },
  { path: 'callback', component: AuthCallback },
];
