import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/combineLatest';
import 'rxjs/add/observable/of';

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
  next?: string;
}

@Injectable()
export class WriterService {
  private nextCache: {
    [key: string]: {
      [key: string]: string,
      nextWriter: string
    }
  } = {};

  constructor(private http: Http) { }

  getList(): Observable<string[]> {
    return this.http.get(`${apiEndpoint}/writers`)
      .map(res => res.json())
      .map(x => {
        x.forEach((writer, index) => {
          this.nextCache[writer] = {
            nextWriter: (index !== x.length - 1) ? `/writer/${x[index + 1]}` : '/'
          };
        });
        return x;
      });
  }

  getWriter(writerId: string): Observable<Writer> {
    return this.http.get(`${apiEndpoint}/writers/${writerId}`)
      .map<any, Writer>(res => res.json())
      .map(x => {
        x.writings.forEach((writing, index) => {
          if (index !== x.writings.length - 1) {
            this.nextCache[x.name][writing] = `/writer/${x.name}/writing/${x.writings[index + 1]}`;
          } else {
            this.nextCache[x.name][writing] = this.nextCache[x.name].nextWriter;
          }
        });
        return x;
      });
  }

  getWriting(writerId: string, writingId: string): Observable<Writing> {
    return this.http.get(`${apiEndpoint}/writers/${writerId}/${writingId}`)
      .map(res => res.json())
      .map((writing: Writing) => ({
        ...writing,
        strokes: writing.strokes.map(stroke => ({
          color: this.getStrokeColor(stroke),
          ...stroke,
          strokeDirection: (stroke.isHorizontal && !stroke.strokeDirection) ? 'unknown' : stroke.strokeDirection
        }))
      }));
  }

  getStrokeColor(stroke: Stroke) {
    if (stroke.isHorizontal) {
      if (stroke.strokeDirection === 'left') {
        return 'green';
      }
      if (stroke.strokeDirection === 'right') {
        return 'blue';
      }
    }
    return 'black';
  }

  removeHorizontalLine(writerId: string, writingId: string, lineIndex: number) {
    return this.http.delete(`${apiEndpoint}/writers/${writerId}/${writingId}/lines/${lineIndex}`);
  }

  addHorizontalLine(writerId: string, writingId: string, lineIndex: number, type: Orientation) {
    return this.http.put(`${apiEndpoint}/writers/${writerId}/${writingId}/lines/${lineIndex}`, {
      type
    });
  }

  changeManualHandedness(writerId: string, writingId: string, type: Orientation) {
    return this.http.put(`${apiEndpoint}/writers/${writerId}/${writingId}`, {
      manualHandedness: type
    });
  }

  getNext(writerId$: Observable<string>, writingId$: Observable<string>) {
    return writerId$.combineLatest(writingId$)
      .mergeMap(([writerId, writingId]) => {
        if (this.nextCache[writerId]) {
          if (this.nextCache[writerId][writingId]) {
            return Observable.of([writerId, writingId]);
          } else {
            return this.getWriter(writerId)
              .map(() => [writerId, writingId]);
          }
        }
        return this.getList()
          .mergeMap(() => this.getWriter(writerId))
          .map(() => [writerId, writingId]);
      })
      .do(() => console.log(this.nextCache))
      .map(([writerId, writingId]) => this.nextCache[writerId][writingId]);
  }
}
