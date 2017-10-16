import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

const apiEndpoint = '/api';

export type Orientation = 'left' | 'right' | 'unknown';

export interface Writer {
  name: string;
  writings: string[];
}

export interface Stroke {
  points: {
    x: number,
    y: number,
    time: string
  }[];
  color: string;
  strokeDirection: Orientation;
  isHorizontal: boolean;
}

export interface Writing {
  writerId: string;
  writingId: string;
  strokes: Stroke[];
  captureTime: Date;
  text: string;
  calculatedHandedness: Orientation;
  algorithmLog: string;
  manualHandedness: Orientation;
}

@Injectable()
export class WriterService {

  constructor(private http: Http) { }

  getList(): Observable<string[]> {
    return this.http.get(`${apiEndpoint}/writers`).map(res => res.json());
  }

  getWriter(writerId: string): Observable<Writer> {
    return this.http.get(`${apiEndpoint}/writers/${writerId}`).map(res => res.json());
  }

  getWriting(writerId: string, writingId: string): Observable<Writing> {
    return this.http.get(`${apiEndpoint}/writers/${writerId}/${writingId}`)
      .map(res => res.json())
      .map((writing: Writing) => ({
        ...writing,
        strokes: writing.strokes.map(stroke => ({
          color: 'black',
          ...stroke,
          strokeDirection: (stroke.isHorizontal && !stroke.strokeDirection) ? 'unknown' : stroke.strokeDirection
        }))
      }));
  }

}
