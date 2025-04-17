import { Injectable } from '@angular/core';
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { HttpMethod } from '@enums/HttpMethod';
import useParser from '../composables/useParser';
import { environment } from 'environment/environment';


const { convertObjectsKeysCase } = useParser;

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http: AxiosInstance;
  private baseURL = environment.apiUrl;


  constructor() {
    this.http = axios.create({
      baseURL: this.baseURL,
      withCredentials: false,
      headers: this.setupHeaders(),
    });
  }

  private get getAuthorization() {
    const accessToken = localStorage.getItem('token');
    return accessToken
      ? { Authorization: `Bearer ${ accessToken }` }
      : {};
  }

  public async get<T>(url: string, hasAttachment = false): Promise<T> {
    return this.request<T>(HttpMethod.GET, url, {
      headers: this.setupHeaders(hasAttachment),
    });
  }

  public async post<T, P>(url: string, payload: P, hasAttachment = false, isUrlEncoded = false): Promise<T> {
    return this.request<T>(HttpMethod.POST, url, {
      data: isUrlEncoded
        ? payload
        : convertObjectsKeysCase(payload, 'snake'),
      headers: this.setupHeaders(hasAttachment, isUrlEncoded),
    });
  }

  public async put<T, P>(url: string, payload: P, hasAttachment = false): Promise<T> {
    return this.request<T>(HttpMethod.PUT, url, {
      data: payload,
      headers: this.setupHeaders(hasAttachment),
    });
  }

  public async delete<T>(url: string, hasAttachment = false): Promise<T> {
    return this.request<T>(HttpMethod.DELETE, url, {
      headers: this.setupHeaders(hasAttachment),
    });
  }

  private setupHeaders(hasAttachment = false, isUrlEncoded = false) {
    if (isUrlEncoded) {
      return { 'Content-Type': 'application/x-www-form-urlencoded', ...this.getAuthorization };
    }

    return hasAttachment
      ? { 'Content-Type': 'multipart/form-data', ...this.getAuthorization }
      : { 'Content-Type': 'application/json', ...this.getAuthorization };
  }

  private async request<T>(method: HttpMethod, url: string, options: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.http.request<T>({
        method,
        url,
        ...options,
      });

      return convertObjectsKeysCase(response.data, 'camel');
    } catch (error) {
      return Promise.reject(error);
    }
  }
}
