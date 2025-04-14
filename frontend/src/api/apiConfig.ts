import { environment } from '../environment/environment';


const REDIRECT_URL = environment.redirectUrl;
export const API_URL = environment.apiUrl;
export const GOOGLE_CLIENT_ID = environment.googleClientId;
export const MICROSOFT_CLIENT_ID = environment.microsoftClientId;
export const MICROSOFT_LOGIN_URL = `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
client_id=${ MICROSOFT_CLIENT_ID }
&response_type=code
&redirect_uri=${ REDIRECT_URL }
&scope=offline_access user.read
&response_mode=query
&prompt=login
&state=microsoft`;
export const GOOGLE_LOGIN_URL = `https://accounts.google.com/o/oauth2/v2/auth?
client_id=${ GOOGLE_CLIENT_ID }
&response_type=code
&redirect_uri=${ REDIRECT_URL }
&scope=openid email profile
&access_type=offline
&prompt=consent
&state=google`;


