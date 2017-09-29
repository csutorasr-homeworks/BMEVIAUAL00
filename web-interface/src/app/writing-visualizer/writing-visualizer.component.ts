import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { Stroke } from '../writer.service';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/combineLatest';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/share';

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
  topOffset: number;
  bottomOffset: number;
  leftOffset: number;
  rightOffset: number;
}

@Component({
  selector: 'app-writing-visualizer',
  templateUrl: './writing-visualizer.component.html',
  styleUrls: ['./writing-visualizer.component.css']
})
export class WritingVisualizerComponent implements OnInit {
  @Input() strokes$: Observable<Stroke[]>;
  @Input() zoom$: Observable<number>;
  svgViewBox$: Observable<string>;
  svgHeight$: Observable<number>;
  svgWidth$: Observable<number>;
  hitBoxWidth$: Observable<number>;
  drawableStrokes$: Observable<DrawableStroke[]>;
  @Output() selected = new EventEmitter<number>();

  constructor() { }

  ngOnInit() {
    const drawData$ = this.strokes$.map(x => this.convertToDrawData(x)).share();
    const drawDataWithZoom$ = Observable.combineLatest(drawData$, this.zoom$).share();
    this.drawableStrokes$ = drawData$.map(x => x.drawableStrokes);
    this.svgWidth$ = drawDataWithZoom$.map(([drawData, zoom]) => (drawData.rightOffset - drawData.leftOffset) * zoom);
    this.svgHeight$ = drawDataWithZoom$.map(([drawData, zoom]) => (drawData.bottomOffset - drawData.topOffset) * zoom);
    this.svgViewBox$ = drawData$.map(x => `${x.leftOffset} ${x.topOffset} ${x.rightOffset - x.leftOffset} ${x.bottomOffset - x.topOffset}`);
    this.hitBoxWidth$ = this.zoom$.map(x => 6 / x);
  }


  convertToDrawableStroke(stroke: Stroke): DrawableStroke {
    const drawableStroke: DrawableStroke = {
      ...stroke,
      drawablePoints: []
    };
    const array = drawableStroke.points;
    for (let i = 0; i < array.length - 1; i++) {
      drawableStroke.drawablePoints.push({
        x1: array[i].x,
        y1: array[i].y,
        x2: array[i + 1].x,
        y2: array[i + 1].y,
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
    return {
      drawableStrokes: strokes.map(stroke => this.convertToDrawableStroke(stroke)),
      topOffset, bottomOffset, leftOffset, rightOffset,
    };
  }

  strokeClicked(index) {
    this.selected.next(index);
  }
}
