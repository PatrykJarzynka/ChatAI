import { environment } from 'environment/environment';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  private configPath = 'assets/config.json';

  constructor(private http: HttpClient) {
  }

  async loadConfig() {
    const config = await firstValueFrom(this.http.get<any>(this.configPath));

    environment.apiUrl = config.API_URL || environment.apiUrl;
    environment.redirectUrl = config.REDIRECT_URL || environment.redirectUrl;
    environment.googleClientId = config.GOOGLE_CLIENT_ID || environment.googleClientId;
    environment.microsoftClientId = config.MICROSOFT_CLIENT_ID || environment.microsoftClientId;
  }

  getGooglePath(): string {
    return `https://accounts.google.com/o/oauth2/v2/auth?client_id=${ environment.googleClientId }&response_type=code&redirect_uri=${ environment.redirectUrl }&scope=openid email profile&access_type=offline&prompt=consent&state=google`;
  }

  getMicrosoftPath(): string {
    return `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=${ environment.microsoftClientId }&response_type=code&redirect_uri=${ environment.redirectUrl }&scope=offline_access user.read&response_mode=query&prompt=login&state=microsoft`;
  }

}
