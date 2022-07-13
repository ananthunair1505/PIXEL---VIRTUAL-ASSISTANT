package main

import (
	"context"
	"fmt"
	"os"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/pkg/errors"
	"github.com/potsbo/jobcan/account"
	"github.com/potsbo/jobcan/config"
)

func jobcanTouch(ctx context.Context, c config.Config) (string, error) {
	if !c.Valid() {
		return "", errors.Errorf("No")
	}
	mode := os.Getenv("JOBCAN_ADIT")
	if len(mode) == 0 {
		return "", errors.Errorf("JOBCAN_ADIT is empty")
	}

	a := account.New(c)
	if err := a.Login(); err != nil {
		return "", errors.Wrap(err, "failed to login")
	}
	if err := a.ExecAttendance(mode); err != nil {
		return "", errors.Wrap(err, "failed to record")
	}
	return fmt.Sprintf("Your \"%s\" has successfully been recorded.", mode), nil
}

func main() {
	lambda.Start(jobcanTouch)
}