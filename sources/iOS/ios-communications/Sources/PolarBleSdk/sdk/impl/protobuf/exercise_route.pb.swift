// DO NOT EDIT.
// swift-format-ignore-file
//
// Generated by the Swift generator plugin for the protocol buffer compiler.
// Source: exercise_route.proto
//
// For information on using the generated types, please see the documentation:
//   https://github.com/apple/swift-protobuf/

/// ROUTE.BPB=PbExerciseRouteSamples

import Foundation
import SwiftProtobuf

// If the compiler emits an error on this type, it is because this file
// was generated by a version of the `protoc` Swift plug-in that is
// incompatible with the version of SwiftProtobuf to which you are linking.
// Please ensure that you are building against the same version of the API
// that was used to generate this file.
fileprivate struct _GeneratedWithProtocGenSwiftVersion: SwiftProtobuf.ProtobufAPIVersionCheck {
  struct _2: SwiftProtobuf.ProtobufAPIVersion_2 {}
  typealias Version = _2
}

///
///Route samples of the exercise.
///! All fields are required.
public struct Data_PbExerciseRouteSamples {
  // SwiftProtobuf.Message conformance is added in an extension below. See the
  // `Message` and `Message+*Additions` files in the SwiftProtobuf library for
  // methods supported on all messages.

  /// Duration of sample from exercise/transition start,taking pauses into account
  /// range [0 - 359999999] (ms), i.e. 00:00:00.000 - 99:59:59.999
  var duration: [UInt32] = []

  /// latitude, value is positive on northern hemisphere
  var latitude: [Double] = []

  /// longitude, value is positive on eastern hemisphere
  var longitude: [Double] = []

  /// gps altitude
  var gpsAltitude: [Int32] = []

  /// number of satellites
  var satelliteAmount: [UInt32] = []

  /// fix status
  var obsoleteFix: [Bool] = []

  /// indicate start and stop indexes when there has not been connection to gps sensor
  var obsoleteGpsOffline: [PbSensorOffline] = []

  /// GPS date and time in UTC
  var obsoleteGpsDateTime: [PbSystemDateTime] = []

  /// GPS date and time of first location point
  var firstLocationTime: PbSystemDateTime {
    get {return _firstLocationTime ?? PbSystemDateTime()}
    set {_firstLocationTime = newValue}
  }
  /// Returns true if `firstLocationTime` has been explicitly set.
  var hasFirstLocationTime: Bool {return self._firstLocationTime != nil}
  /// Clears the value of `firstLocationTime`. Subsequent reads from it will return its default value.
  mutating func clearFirstLocationTime() {self._firstLocationTime = nil}

    public var unknownFields = SwiftProtobuf.UnknownStorage()

    public init() {}

  fileprivate var _firstLocationTime: PbSystemDateTime? = nil
}

#if swift(>=5.5) && canImport(_Concurrency)
extension Data_PbExerciseRouteSamples: @unchecked Sendable {}
#endif  // swift(>=5.5) && canImport(_Concurrency)

// MARK: - Code below here is support for the SwiftProtobuf runtime.

fileprivate let _protobuf_package = "data"

extension Data_PbExerciseRouteSamples: SwiftProtobuf.Message, SwiftProtobuf._MessageImplementationBase, SwiftProtobuf._ProtoNameProviding {
    public static let protoMessageName: String = _protobuf_package + ".PbExerciseRouteSamples"
    public static let _protobuf_nameMap: SwiftProtobuf._NameMap = [
    1: .same(proto: "duration"),
    2: .same(proto: "latitude"),
    3: .same(proto: "longitude"),
    4: .standard(proto: "gps_altitude"),
    5: .standard(proto: "satellite_amount"),
    6: .standard(proto: "OBSOLETE_fix"),
    7: .standard(proto: "OBSOLETE_gps_offline"),
    8: .standard(proto: "OBSOLETE_gps_date_time"),
    9: .standard(proto: "first_location_time"),
  ]

  public var isInitialized: Bool {
    if !SwiftProtobuf.Internal.areAllInitialized(self.obsoleteGpsOffline) {return false}
    if !SwiftProtobuf.Internal.areAllInitialized(self.obsoleteGpsDateTime) {return false}
    if let v = self._firstLocationTime, !v.isInitialized {return false}
    return true
  }

    mutating public func decodeMessage<D: SwiftProtobuf.Decoder>(decoder: inout D) throws {
    while let fieldNumber = try decoder.nextFieldNumber() {
      // The use of inline closures is to circumvent an issue where the compiler
      // allocates stack space for every case branch when no optimizations are
      // enabled. https://github.com/apple/swift-protobuf/issues/1034
      switch fieldNumber {
      case 1: try { try decoder.decodeRepeatedUInt32Field(value: &self.duration) }()
      case 2: try { try decoder.decodeRepeatedDoubleField(value: &self.latitude) }()
      case 3: try { try decoder.decodeRepeatedDoubleField(value: &self.longitude) }()
      case 4: try { try decoder.decodeRepeatedSInt32Field(value: &self.gpsAltitude) }()
      case 5: try { try decoder.decodeRepeatedUInt32Field(value: &self.satelliteAmount) }()
      case 6: try { try decoder.decodeRepeatedBoolField(value: &self.obsoleteFix) }()
      case 7: try { try decoder.decodeRepeatedMessageField(value: &self.obsoleteGpsOffline) }()
      case 8: try { try decoder.decodeRepeatedMessageField(value: &self.obsoleteGpsDateTime) }()
      case 9: try { try decoder.decodeSingularMessageField(value: &self._firstLocationTime) }()
      default: break
      }
    }
  }

    public func traverse<V: SwiftProtobuf.Visitor>(visitor: inout V) throws {
    // The use of inline closures is to circumvent an issue where the compiler
    // allocates stack space for every if/case branch local when no optimizations
    // are enabled. https://github.com/apple/swift-protobuf/issues/1034 and
    // https://github.com/apple/swift-protobuf/issues/1182
    if !self.duration.isEmpty {
      try visitor.visitPackedUInt32Field(value: self.duration, fieldNumber: 1)
    }
    if !self.latitude.isEmpty {
      try visitor.visitRepeatedDoubleField(value: self.latitude, fieldNumber: 2)
    }
    if !self.longitude.isEmpty {
      try visitor.visitRepeatedDoubleField(value: self.longitude, fieldNumber: 3)
    }
    if !self.gpsAltitude.isEmpty {
      try visitor.visitPackedSInt32Field(value: self.gpsAltitude, fieldNumber: 4)
    }
    if !self.satelliteAmount.isEmpty {
      try visitor.visitPackedUInt32Field(value: self.satelliteAmount, fieldNumber: 5)
    }
    if !self.obsoleteFix.isEmpty {
      try visitor.visitPackedBoolField(value: self.obsoleteFix, fieldNumber: 6)
    }
    if !self.obsoleteGpsOffline.isEmpty {
      try visitor.visitRepeatedMessageField(value: self.obsoleteGpsOffline, fieldNumber: 7)
    }
    if !self.obsoleteGpsDateTime.isEmpty {
      try visitor.visitRepeatedMessageField(value: self.obsoleteGpsDateTime, fieldNumber: 8)
    }
    try { if let v = self._firstLocationTime {
      try visitor.visitSingularMessageField(value: v, fieldNumber: 9)
    } }()
    try unknownFields.traverse(visitor: &visitor)
  }

    public static func ==(lhs: Data_PbExerciseRouteSamples, rhs: Data_PbExerciseRouteSamples) -> Bool {
    if lhs.duration != rhs.duration {return false}
    if lhs.latitude != rhs.latitude {return false}
    if lhs.longitude != rhs.longitude {return false}
    if lhs.gpsAltitude != rhs.gpsAltitude {return false}
    if lhs.satelliteAmount != rhs.satelliteAmount {return false}
    if lhs.obsoleteFix != rhs.obsoleteFix {return false}
    if lhs.obsoleteGpsOffline != rhs.obsoleteGpsOffline {return false}
    if lhs.obsoleteGpsDateTime != rhs.obsoleteGpsDateTime {return false}
    if lhs._firstLocationTime != rhs._firstLocationTime {return false}
    if lhs.unknownFields != rhs.unknownFields {return false}
    return true
  }
}
