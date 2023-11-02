/**
 * @license
 * Copyright Google LLC All Rights Reserved.
 *
 * Use of this source code is governed by an MIT-style license that can be
 * found in the LICENSE file at https://angular.io/license
 */

import {Component, ViewEncapsulation} from '@angular/core';

/** Root component for the dev-app demosa. */
@Component({
  selector: 'will',
  template: '<div>hi</div>',
  encapsulation: ViewEncapsulation.None,
  standalone: true,
})
export class DevApp {}
