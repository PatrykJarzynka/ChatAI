import { Injectable } from '@angular/core';
import { ApiService } from '@services/ApiService';


@Injectable({
  providedIn: 'root'
})
export class FileValidator {
  allowedFileFormats: string[] = ['txt', 'pdf'];
  maxFileSize: number = 5_242_880;

  constructor(private apiService: ApiService) {
  }

  validateFile(file: File): boolean {
    let valid = true;

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

    return valid;
  }
}

