import inquirer from "inquirer";
import chalk from "chalk";

// enum SequenceMode {
//   "auto",
//   "custom"
// }

class Bit {
  constructor(
    public readonly position: number,
    public readonly value: number,
    public readonly isControlBit: boolean = false,
    public readonly corrected: boolean = false
  ) {}
}

type sequencePrimitive = string;

class Sequence {
  private readonly _sequence: Bit[];

  get correctedFullSequence(): Bit[] {
    const errorPosition = this.getErrorPosition();
    if (errorPosition === null) {
      return this._sequence
    }
    const readyToCorrect = [...this._sequence];
    readyToCorrect.splice(
      errorPosition,
      1,
      new Bit(
        errorPosition,
        this.flipBitAt(errorPosition),
        this.isControlBit(errorPosition),
        true
      )
    );
    console.log(readyToCorrect)
    return readyToCorrect;
  }

  get corrected() {
    return [...this.getInfoBits(this.correctedFullSequence)];
  }

  get originalSequence(): string {
    return this._sequence.reduce((acc, cur) => acc + cur.value.toString(), "");
  }

  private flipBitAt(position: number) {
    return +!this.getBitAt(position);
  }

  constructor(sequence: sequencePrimitive) {
    this.verify(sequence);

    this._sequence = [];
    for (let i = 0; i < sequence.length; i++) {
      this._sequence.push(
        new Bit(
          i,
          parseInt(sequence[i], 2),
          this.isControlBit(i, sequence.length)
        )
      );
    }
  }

  private verify(sequence: sequencePrimitive) {
    const binSequence = parseInt(sequence, 2);
    if (isNaN(binSequence)) {
      throw new Error(`sequence ${sequence} is invalid`);
    }

    if (sequence.length !== 7) {
      throw new Error(`expected sequence of length 7; got ${sequence.length}`);
    }
  }

  *getControlBits() {
    for (const position of this.getControlBitPositions()) {
      yield new Bit(position, this.getBitAt(position), true);
    }
  }

  *getInfoBits(sequence?: Bit[]) {
    yield* (sequence ?? this._sequence).filter((bit) => !bit.isControlBit);
  }

  private isControlBit(position: number, length?: number): boolean {
    // faster solution: (x != 0) && ((x & (x - 1)) == 0)
    const controlBitPositions = [
      ...this.getControlBitPositions(length ?? this._sequence.length),
    ];

    return controlBitPositions.includes(position);
  }

  private *getControlBitPositions(length?: number) {
    for (
      let i = 0, position = 2 ** i - 1;
      position < (length ?? this._sequence.length);
      i++, position = 2 ** i - 1
    ) {
      yield position;
    }
  }

  private getBitAt(position: number, sequence?: Bit[]): number {
    return (sequence ?? this._sequence)[position].value;
  }

  /** Position is relative to full sequence */
  getErrorPosition() {
    const totalSymptom = [];

    for (let i = 1; i <= this.getAmountOfSymptoms(); i++) {
      totalSymptom.push(this.getSymptom(i));
    }

    const symptom = parseInt(totalSymptom.reverse().join(""), 2);
    if (symptom === 0) {
      return null
    }
    return symptom - 1;
  }

  private getSymptom(symptom: number) {
    return (
      this.getBitsOfSymptom(symptom).reduce(
        (previous, current) => previous + current,
        0
      ) % 2
    );
  }

  private getBitsOfSymptom(symptom: number) {
    if (symptom > this.getAmountOfSymptoms()) {
      throw new Error(
        `sequence ${
          this.originalSequence
        } has only ${this.getAmountOfSymptoms()} symptoms; got ${symptom}`
      );
    }

    const bits = [];

    const step = 2 ** (symptom - 1);
    const startingPosition = step - 1;

    for (
      let basePosition = startingPosition;
      basePosition <= this._sequence.length;
      basePosition += step * 2
    ) {
      for (let offset = 0; offset < step; offset++) {
        const position = offset + basePosition;
        bits.push(this.getBitAt(position));
      }
    }

    return bits;
  }

  private getAmountOfSymptoms() {
    return [...this.getControlBits()].length;
  }
}

const answers = await inquirer.prompt([
  {
    type: "string",
    name: "input-sequence",
    message: "Введите сообщение закодированное кодом Хэмминга",
    default: "0000000",
  },
]);

try {
  const test = new Sequence(answers["input-sequence"]);

  console.log(
    test.corrected
      .map((bit) =>
        bit.corrected ? chalk.red(bit.value) : bit.value.toString()
      )
      .join("")
  );
} catch (error) {
  console.error((<Error>error).message);
  console.error(error)
}
