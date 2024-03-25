package main

import (
	"fmt"
	"io/fs"
	"os"
	"reflect"
)

type folder struct {
	File    os.FileInfo
	Folders []folder
}

func tree(str string) []fs.DirEntry {
	a, err := os.ReadDir(str)
	if err != nil {
		return nil
	}
	return a
}

func getFolders() {

}

func main() {
	b := tree("./123")
	// if err != nil {
	// 	return
	// }
	fmt.Println(reflect.TypeOf(b))
}
