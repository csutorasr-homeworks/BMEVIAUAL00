import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import 'rxjs/add/operator/mergeMap';
import 'rxjs/add/operator/pairwise';
import 'rxjs/add/operator/share';
import 'rxjs/add/operator/toArray';

import { WriterService, Stroke } from '../writer.service';
import { Observable } from 'rxjs/Observable';

interface DrawableStroke extends Stroke {
  drawablePoints: {
    x1: number,
    y1: number,
    x2: number,
    y2: number
  }[];
}

interface DrawData {
  drawableStrokes: DrawableStroke[];
  width: number;
  height: number;
}

@Component({
  selector: 'app-writing',
  templateUrl: './writing.component.html',
  styleUrls: ['./writing.component.css']
})
export class WritingComponent implements OnInit {
  svgHeight$: Observable<number>;
  svgWidth$: Observable<number>;
  strokes$: Observable<DrawableStroke[]>;
  text$: Observable<string>;
  writerId$: Observable<string>;

  constructor(private activatedRoute: ActivatedRoute, private writerService: WriterService, private router: Router) { }

  ngOnInit() {
    const writing$ = this.activatedRoute.params
      .mergeMap(x => this.writerService.getWriting(x.writerId, x.writingId)).share();
    this.writerId$ = writing$.map(x => x.writerId);
    this.text$ = writing$.map(x => x.text);
    const drawData = writing$.map(x => this.convertToDrawData(x.strokes));
    this.strokes$ = drawData.map(x => x.drawableStrokes);
    this.svgWidth$ = drawData.map(x => x.width);
    this.svgHeight$ = drawData.map(x => x.height);
  }

  convertToDrawableStroke(stroke: Stroke, leftOffset: number, topOffset: number, zoom: number): DrawableStroke {
    const drawableStroke: DrawableStroke = {
      ...stroke,
      drawablePoints: []
    };
    const array = drawableStroke.points;
    for (let i = 0; i < array.length - 1; i++) {
      drawableStroke.drawablePoints.push({
        x1: (array[i].x - leftOffset) * zoom,
        y1: (array[i].y - topOffset) * zoom,
        x2: (array[i + 1].x - leftOffset) * zoom,
        y2: (array[i + 1].y - topOffset) * zoom,
      });
    }
    return drawableStroke;
  }

  convertToDrawData(strokes: Stroke[]): DrawData {
    let topOffset = 0, rightOffset = 0, bottomOffset = 0, leftOffset = 0;
    const strokeWithPoint = strokes.find(stroke => stroke.points.length > 0);
    if (strokeWithPoint !== undefined) {
      topOffset = strokeWithPoint.points[0].y;
      bottomOffset = strokeWithPoint.points[0].y;
      rightOffset = strokeWithPoint.points[0].x;
      leftOffset = strokeWithPoint.points[0].x;
    }
    strokes.forEach(stroke => stroke.points.forEach(point => {
      if (point.y < topOffset) {
        topOffset = point.y;
      }
      if (bottomOffset < point.y) {
        bottomOffset = point.y;
      }
      if (point.x < leftOffset) {
        leftOffset = point.x;
      }
      if (rightOffset < point.x) {
        rightOffset = point.x;
      }
    }));
    const zoom = 0.1;
    return {
      drawableStrokes: strokes.map(stroke => this.convertToDrawableStroke(stroke, leftOffset, topOffset, zoom)),
      width: (leftOffset - rightOffset) * zoom,
      height: (bottomOffset - topOffset) * zoom
    };
  }
}
