import { Injectable } from '@angular/core';
import { UploadResponse } from '@appTypes/UploadResponse';
import { ApiService } from '@services/ApiService';


@Injectable({
  providedIn: 'root',
})
export class FileUploader {

  constructor(private apiService: ApiService) {
  }

  async upload(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return await this.apiService.post<UploadResponse, FormData>('/file', formData, true, true);
  }
}
