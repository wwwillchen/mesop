import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ChannelService } from "../../../web/src/services/channel_service";

@Component({
  selector: "app-foo-bar",
  templateUrl: "foo_bar.html",
  standalone: true,
})
export class FooBarComponent {
  @Input() config!: pb.FooBarComponent;

  constructor(private readonly channelService: ChannelService) {}

  handleClick(event: any) {}
}
