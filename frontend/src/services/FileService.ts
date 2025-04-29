import { Injectable } from '@angular/core';
import { ApiService } from '@services/ApiService';


@Injectable({
  providedIn: 'root'
})
export class FileService {
  allowedFileFormats: string[] = [];
  maxFileSize: number = 5_242_880;

  constructor(fileFormats: string[], private apiService: ApiService) {
    this.allowedFileFormats = fileFormats;
  }

  validateFiles(files: File[]): boolean {
    let valid = true;

    files.forEach(file => {
      const fileName = file.name;
      const fileExtension = fileName.split('.')[fileName.split('.').length - 1].toLowerCase();
      const fileSize = file.size;

      if (!this.allowedFileFormats.includes(fileExtension)) {
        valid = false;
        console.error(`Invalid file extension for file: ${ fileName }`);
      }

      if (fileSize > this.maxFileSize) {
        valid = false;
        console.error(`Invalid file size for file: ${ fileName }`);
      }
    });

    return valid;
  }

  uploadFiles(files: File[]): void {
    const validState = this.validateFiles(files);

    if (validState) {
      // this.apiService.post();
    }
  }
}

