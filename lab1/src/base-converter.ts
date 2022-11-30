import inquirer from "inquirer";
import chalk from "chalk";


// modify base string class to add count() method
declare global {
  interface String {
    count: (this: string, sub: string) => number;
  }
}

String.prototype.count = function (sub: string): number {
  let cursor = 0;
  let count = 0;

  while (this.includes(sub, cursor)) {
    cursor = this.indexOf(sub, cursor) + sub.length;
    count++;
  }

  return count;
};

/** Performs conversion of numbers*/
class UniversalNumber {
  private store: DigitStore;

  constructor(n: number);
  constructor(n: string | DigitStore, base: number);
  constructor(n: string | DigitStore | number, private fromBase: number = 10) {
    if (n instanceof DigitStore) {
      this.store = n;
    } else {
      if (typeof n === "number") {
        n = n.toString();
      }
      this.store = DigitStore.buildFrom(n.toUpperCase());
    }

    this.store.checkAgainstBase(fromBase);
  }

  convertToBase(base: number, accuracy?: number): [string, string] {
    return [
      this.convertFromDecimalInt(base).toHumanDigits(),
      this.convertFromDecimalFr(base, accuracy).toHumanDigits(),
    ];
  }

  private convertFromDecimalFr(base: number, accuracy: number = 5) {
    let n = this.store.fr.convertToDecimal(this.fromBase);
    const result: number[] = [];

    for (let i = 0; i < accuracy && n > 0; i++) {
      const multiplied = n * base;
      result.push(Math.trunc(multiplied))
      n = multiplied % 1
    }

    return new DigitSequence(result);
  }

  private convertFromDecimalInt(base: number) {
    let n = this.store.int.convertToDecimal(this.fromBase);
    const result: number[] = [];

    while (n != 0) {
      result.push(n % base);
      n = Math.floor(n / base);
    }

    return new DigitSequence(result.reverse());
  }

}

class DigitStore {
  constructor(
    public int: IntDigitSequence = new IntDigitSequence([0]),
    public fr: FrDigitSequence = new FrDigitSequence([0])
  ) {}

  checkAgainstBase(base: number) {
    const digits = this.int.digits.concat(this.fr.digits);
    for (let i = 0; i < digits.length; i++) {
      const digit = digits[i];
      if (digit.value >= base) {
        throw new SyntaxError(
          `Digit ${digit.toHumanDigit()} on position ${
            i >= this.int.digits.length ? i + 1 : i
          } is not allowed in numeric system with base ${base}`
        );
      }
    }
  }

  static buildFrom(input: string): DigitStore {
    const separators = ".,";

    for (const separator of separators) {
      if (input.count(separator) > 1) {
        throw new Error(
          'only one separator (i.e. "." or ",") in a number is allowed'
        );
      }

      if (input.includes(separator)) {
        const parts = input.split(separator)

        return new DigitStore(
          new IntDigitSequence(parts[0]),
          new FrDigitSequence(parts[1])
        );
      }
    }

    return new DigitStore(new IntDigitSequence(input), new FrDigitSequence([0]));
  }
}

class DigitSequence {
  digits: Digit[]

  constructor(input: string | number[]) {
    this.digits = []
    if (input instanceof Array) {
      this.digits.push(...input.map((digit) => new Digit(digit)));
    } else {
      this.digits.push(...input.split("").map((digit) => new Digit(digit)));
    }
  }

  toHumanDigits(): string {
    return this.digits.map((digit) => digit.toHumanDigit()).join("");
  }
}

class IntDigitSequence extends DigitSequence {
  convertToDecimal(base: number) {
    const int = [...this.digits].reverse()
    let intResult = 0;
    for (let i = 0; i < int.length; i++) {
      intResult += int
      [i].value * base ** i;
    }

    return intResult;
  }
}

class FrDigitSequence extends DigitSequence {
  convertToDecimal(base: number) {
    let fractional = [...this.digits]

    let frResult = 0;
    for (let i = 0; i < fractional.length; i++) {
      frResult += fractional[i].value * base ** flipExtent(i);
    }

    function flipExtent(extent: number) {
      return extent * -1 - 1;
    }
    return frResult;
  }
}

class Digit {
  private static dictionary = "0123456789ABCDEF";
  public value: number;

  constructor(digit: string | number) {
    if (typeof digit === "number") {
      this.value = digit;
    } else {
      this.value = Digit.dictionary.indexOf(digit);
    }
  }

  toHumanDigit() {
    return Digit.dictionary[this.value];
  }
}

const answers = await inquirer.prompt([
  {
    type: "number",
    name: "from-base",
    message: "укажите основание числа",
    default: 10,
    prefix: "From:",
  },
  {
    type: "input",
    name: "from-number",
    message: "введите число",
    default: "0",
    prefix: "From:",
  },
  {
    type: "number",
    name: "to-base",
    message: "укажите основание системы счисления, в которую надо перевести число",
    default: 10,
    prefix: "To:",
  },
]);

console.log();

try {
  const result = new UniversalNumber(
    answers["from-number"],
    answers["from-base"]
  ).convertToBase(answers["to-base"]);

  if (result[1].length === 0) {
    printColorized(result[0]);
  } else {
    printColorized(result.join("."));
  }

  function printColorized(...message: any[]) {
    console.log(chalk.cyanBright(...message));
  }
} catch (error: any) {
  console.error(chalk.red("ERROR: " + error.message));
}
